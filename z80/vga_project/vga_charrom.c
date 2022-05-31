#include  "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/gpio.h"
#include "hardware/clocks.h"
#include "hardware/dma.h"
#include "hardware/structs/bus_ctrl.h"
#include "pico/multicore.h"
#include "rgb.pio.h"
#include "sync.pio.h"
#include "font.h"
#include <stdio.h>
#include <string.h>
#include "z80io.pio.h"
//Goal is to create functions that 
//create buffers with the timing pixels
//embedded. 

//Ex. a 640x480@60hz has 800 pixels per line
//640 visible (RGB values, but no H&V sync)
//16 Front porch, 96 sync pulse, 48 back porch
//after 480 of these lines, we have a few vblank lines
//10 Front porch (hsync normal), 2 sync pulse (vsync and hysnc), 33 back porch

//The PIO must change pin values every
// (1/25.175mhz)s

//the pico defaults to 125mhz.
//code given in datasheet...
//float freq = 25175000
//float div = clock_get_hz(clk_sys) / ();
//     sm_config_set_clkdiv(&c, div)


//we pregenerate several lines, give them to the
//dma engine, then prepare several more
//until we've done enough lines it's time
//for a vsync

//My first mode will use 160x120 upscaled to 
//640x480 as my monitors do not aspect correct
//lower. Each pixel from the z80 will be x4
//and every scanline will repeat 4x. The pico
//only has 240k RAM. 

//Our Dma buffers Will take ~1kb per line. 

//Hsync pin is first, vsync pin is second
//480 lines of hsync buffer
//10 lines of blank, with hsync lines
//and 0s on RGB pins
//2 lines of vsync buffer
//33 back porch  - normal hsync lines

//need to be divisible by 4 for simplest possible pio. 
//dma buffers
uint32_t t_color[] = { 0x00000000,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0xFFFFFFFF
};

uint32_t bt_color[] = { 0x00000000,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0x02020202,
			 0xC0C0C0C0,
			 0x38383838,
			 0xFFFFFFFF
};
			

uint8_t RGB_buffer[2][800]; //8bpp
uint8_t Vblank[800];   //8bpp, 0s
uint8_t Hsync_buffer[200]; //2bpp(HVHVHVHV)
uint8_t Vsync_buffer[200]; //2bpp 


uint32_t unpacked_font[8400];
uint32_t unpacked_mask[8400];
//character buffer
char sbuffer[2401];
//attribute buffer
char abuffer[2401];
//cursor
uint cursor;
uint mode;

#define T_MONOCHROME 0;
#define T_64C_80x30 1;  //2grb, 2status

void generate_rgb_scan(uint8_t *);
void generate_vblank_rgb(uint8_t *);
void generate_hsync_scan(uint8_t *);
void generate_vsync_scan(uint8_t *);


void fill_background() {
  for (int i =0; i < 25; i++)
    for (int j = 0;  j < 80; j++) {
      sbuffer[(i*j)+i] =' ' ;
    }
  //static string.
  strcpy(sbuffer, "Initial buffer - IO 39-10 to reset");
}

void unpack_font() {
  uint8_t buffer[8];
  uint8_t mask[8];
  uint8_t offs;
  for (int i = 0; i < 256; i++) {
    for (int l = 0;l< 16;l++) {      
      offs = VGA8_F16[(i*16)+l];
      buffer[7] = offs & 0x01 ? 255: 0;
      mask[7] = offs & 0x01 ? 0: 255;
      buffer[6] = offs & 0x02 ? 255: 0;
      mask[6] = offs & 0x02 ? 0:255;
      buffer[5] = offs & 0x04 ? 255: 0;
      mask[5] = offs & 0x02 ? 0:255;
      buffer[4] = offs & 0x08 ? 255: 0;
      mask[4] = offs & 0x02 ? 0:255;
      buffer[3] = offs & 0x10 ? 255: 0;
      mask[3] = offs & 0x02 ? 0:255;
      buffer[2] = offs & 0x20 ? 255: 0;
      mask[2] = offs & 0x02 ? 0:255;
      buffer[1] = offs & 0x40 ? 255: 0;
      mask[1] = offs & 0x02 ? 0:255;
      buffer[0] = offs & 0x80 ? 255: 0;
      mask[0] = offs & 0x02 ? 0:255;
      unpacked_font[((i*2)*16)+(l*2)] = *((uint32_t *) buffer);
      unpacked_font[((i*2)*16)+(l*2)+1] = *((uint32_t *) (buffer+4));
      unpacked_mask[((i*2)*16)+(l*2)] = *((uint32_t *) mask);
      unpacked_mask[((i*2)*16)+(l*2)+1] = *((uint32_t *) (mask+4));
    }
  }
}

//fill DMA buffer at current scanline
void fill_scan_m(uint8_t *buffer, char *string, int line) {
  unsigned int p;
  uint32_t *b= (uint32_t *) buffer;
  uint32_t offs;
  for (int i =0; i < 80; i++) {
    p = 2*i;
    offs = ((string[i]*2)*16)+(2*line);
    b[p] = unpacked_font[offs];
    b[p+1] = unpacked_font[offs+1];    
  }
}


void fill_scan(uint8_t *buffer, char *string, char*attr, int line) {
  unsigned int p;

  uint32_t *b= (uint32_t *) buffer;
  uint8_t stats;
  uint32_t offs;
  uint32_t foreground =  0xC0C0C0C0;
  uint32_t background =  0x02020202;
  for (int i =0; i < 80; i++) {
    p = 2*i;    
    offs = ((string[i]*2)*16)+(2*line);
    stats = attr[i];
    if (stats){
      foreground = t_color[stats & 0x0F];
      background = bt_color[(stats & 0xF0) >> 4];
    }
    else {
      foreground = 0xFFFFFFFF;
      background = 0x00000000;
	
    }
      
    b[p] = unpacked_font[offs] & foreground | (unpacked_mask[offs] & background);  
    b[p+1] = unpacked_font[offs+1] & foreground | (unpacked_mask[offs+1] & background);         
  }
}


//bus protocol uses pio1
PIO p1;
uint offset_z80io;
uint sm_z80io;	  

void z80io_setup() {
  //  stdio_init_all();
  float freq = 80000000.0;
  float div = (float)clock_get_hz(clk_sys) / freq;
  //gpio_set_dir(13,0);
  p1 = pio1;
  offset_z80io = pio_add_program(p1, &z80io_program);
  sm_z80io = pio_claim_unused_sm(p1, true);	  

  gpio_init(12);
  gpio_init(11);
  gpio_init(10);
  gpio_set_dir(11,GPIO_OUT);	
  gpio_set_dir(10,GPIO_IN);
  gpio_put(11,1);
  gpio_set_dir(12,GPIO_IN);  
  gpio_pull_up(12);
//  gpio_pull_down(10);  
//for (int i = 0; i < 8; i++) gpio_set_dir(14+i,0);
  z80io_init(p1, sm_z80io, offset_z80io, div);
  pio_sm_set_enabled(p1, sm_z80io, true);    
}



void bus_read() {
  uint32_t r1,r2,r3,r4;
  uint8_t base;
  uint8_t regs[4];
  if(pio_interrupt_get(p1, 5)){      
    r1 = pio_sm_get(p1,sm_z80io);
    base = (uint8_t)((r1 & 0x0000FF00) >> 8);
    regs[base] = (uint8_t) r1 & 0x000000FF;     
    if (base==0){
      sbuffer[cursor++]=regs[base];
      if (cursor >= 2400) cursor = 0;
    }
    if (base==1){
      if (cursor!=0)
	abuffer[cursor-1]=regs[base];
      else
	abuffer[2400]=regs[base];
    }
    if (base==3){
      if (regs[base]==10)
	cursor=0;
    }
    pio_interrupt_clear(p1, 5);      
  }
  if(pio_interrupt_get(p1, 6)) {	
    r1 = pio_sm_get(p1,sm_z80io);
    base = (uint8_t)((r1 & 0x0000FF00) >> 8);		  
    //	printf("(in) %d, base - %d, val - %d, count - %d\r\n", r1, base, regs[base],r4++ );
    if (cursor!=0) r1 = sbuffer[cursor-1];
    else r1=sbuffer[2399];
    r2 = r1 << 24 | r1 << 16 | r1 <<8 | r1;		  
    pio_sm_put(p1, sm_z80io, r2);
    pio_interrupt_clear(p1,6);				
  }
}


//uses pio1

int main(){
//our output is 480 lines of rgb and hsync.
//10 lines of vblank and hsync
//2 lines of vblank and vsync
//33 lines of vblank and hsync
//  char th[] = "This is the message I'd like to repeat. 1234567890\xb0\xb1\xBB";

  set_sys_clock_khz(220000, true);
  unpack_font();
  generate_rgb_scan(RGB_buffer[0]);
	generate_rgb_scan(RGB_buffer[1]);
	generate_vblank_rgb(Vblank);
	generate_hsync_scan(Hsync_buffer);
	generate_vsync_scan(Vsync_buffer);	
	fill_background();
	fill_scan(RGB_buffer[0],sbuffer,abuffer,0);
	fill_scan(RGB_buffer[1],sbuffer,abuffer,0);
	PIO pio = pio0;
	float freq = 25000000.0;
	float div1 = ((float)clock_get_hz(clk_sys)) / freq;
	float div2 = ((float)clock_get_hz(clk_sys)) / freq;
	uint offset_rgb = pio_add_program(pio, &rgb_program);
	uint offset_sync = pio_add_program(pio, &sync_program);
	uint sm_sync = pio_claim_unused_sm(pio, true);
	uint sm_rgb = pio_claim_unused_sm(pio, true);
	//must be started in this order
	rgb_program_init(pio, sm_rgb, offset_rgb, 0, div2);
	sync_program_init(pio, sm_sync, offset_sync, 8, div1);
	//make sure fifos have something in them
	uint32_t blank = 0;
	uint8_t blank8 = 0;
	//to keep in sync, rgb needs 4x the data (2 bits per 8 bits)  
	//overfill in case too much gets shifted out b4 dma start
	pio_sm_put(pio, sm_rgb, blank);
	pio_sm_put(pio, sm_rgb, blank);
	pio_sm_put(pio,sm_rgb, blank);
	pio_sm_put(pio, sm_sync, blank8);
	pio_sm_put(pio, sm_sync, blank8);
	pio_sm_put(pio, sm_sync, blank8);

	//claim RGB DMA Channel, and configure	
    	int rgb_dma_chan = dma_claim_unused_channel(true);
	dma_channel_config dcrgb = dma_channel_get_default_config(rgb_dma_chan);
	channel_config_set_transfer_data_size(&dcrgb, DMA_SIZE_32);
	channel_config_set_write_increment(&dcrgb, false);
	channel_config_set_read_increment(&dcrgb, true);
					//pio, state machine, is_tx
	channel_config_set_dreq(&dcrgb, pio_get_dreq(pio,sm_rgb, true));

	dma_channel_configure(
	        rgb_dma_chan,
	        &dcrgb,
	        &pio0_hw->txf[sm_rgb], // Write address (only need to set this once)
	        NULL,             // Don't provide a read address yet
	        200,              //count
	        false             // Don't start yet
	);
	//same for sync
	int sync_dma_chan = dma_claim_unused_channel(true);
	dma_channel_config dcsync = dma_channel_get_default_config(sync_dma_chan);
	channel_config_set_transfer_data_size(&dcsync, DMA_SIZE_8);
	channel_config_set_write_increment(&dcsync, false);
	channel_config_set_read_increment(&dcsync, true);
	channel_config_set_dreq(&dcsync, pio_get_dreq(pio, sm_sync, true));
	dma_channel_configure (
		sync_dma_chan, 
		&dcsync,
		&pio0_hw->txf[sm_sync],
		NULL,
		200,
		false
	);



//start RGB first then sync so synchronized


	uint16_t scanline = 0;
	uint16_t buffer_line =0;
	uint16_t pixel = 0;
	uint32_t *rgb;
	uint8_t *sync;	
	uint32_t flip = 0;
	//	multicore_launch_core1(z80io_core_entry);
	z80io_setup();
	pio_sm_set_enabled(pio, sm_rgb, true);
	pio_sm_set_enabled(pio, sm_sync, true);
	fill_scan((uint8_t *)RGB_buffer[0], sbuffer, abuffer, 0);
	fill_scan((uint8_t *)RGB_buffer[1], sbuffer, abuffer, 0);

	uint32_t bstart = 0;
	uint32_t bold =0;
	uint32_t vb;
	while (1) {
	 
	  if (scanline <  480) {
	    vb=0;
	    bstart = (scanline / 16)*80;
	    if (flip==1)flip=0;
	    else if (flip==0)flip=1;
	    rgb = (uint32_t *) RGB_buffer[flip];	    
	    sync = Hsync_buffer;
	  }
	  
	  else if (scanline  < 490) {
	    vb=1;
	    rgb = (uint32_t *) Vblank;
	    sync = Hsync_buffer;
		
	  }
	  else if (scanline < 492) {

	    rgb = (uint32_t *) Vblank;
	    sync = Vsync_buffer;
	  }
	  
	  else if (scanline < 525) {

	    rgb = (uint32_t *) Vblank;
	    sync = Hsync_buffer;
	    
	  }
	  else {
	    scanline =0;
	    vb=0;
	    //continue;
	  }
	  //we could alternate buffers, assign blocks, etc. 
	  dma_channel_set_read_addr(rgb_dma_chan, rgb, true);
	  dma_channel_set_read_addr(sync_dma_chan, sync, true);
	  //fill the buffer for the flip
	  scanline++;
	  if (!vb){
	    fill_scan(RGB_buffer[((flip+1)%2)], (char *)(sbuffer+bstart),
		      (char *)(abuffer+bstart),scanline%16);
	    while(dma_channel_is_busy(rgb_dma_chan)){
	      bus_read();
	    }
	  }
	  else{
	    while(dma_channel_is_busy(rgb_dma_chan))
	      bus_read();
	  }
	  //dma_channel_wait_for_finish_blocking(rgb_dma_chan);
	  dma_channel_wait_for_finish_blocking(sync_dma_chan);
	  
	  
	}
}
//we  use the same buffer for 
//hysnc and vsync
//656 high, 96 low, 48 high
//640, 16, 96, 48
//200 bytes 

//to avoid synchronization issues, pad out to full length
//void generate_hsync_line(uint8_t *);
void generate_rgb_scan (uint8_t * buffer) {
	for (int i =0; i < 640; i++) {
	int val = i/160;
	switch (val){
		case 0:
			buffer[i] = 0;
			break;
		case 1:
			buffer[i] = 0xff;
			break;
		case 2: 
			buffer[i] = 0xFB;
			break;
		case 3:
			buffer[i] = 0x09;
	}
	}
	for (int i=640; i < 800; i++) {
		buffer[i] = 0;
	}
}

void generate_vblank_rgb(uint8_t * buffer) {
	for (int i=0; i< 800; i++)
		buffer[i]=0;
}

void generate_hsync_scan(uint8_t * buffer) {
	//visible 80 bytes 0
	//two bits in buffer per pixel. 
	//two bytes per 8 pixels
	//160 bytes for visible (0)
	//four bytes for front_por (0)
	//96 pixels 24 bytes (10101010)	
	//48 pixels, 12 bytes 0
	for (int i = 0; i < 164; i++) {
		buffer[i] = 0xFF;
	}
	for (int i= 164; i < 188; i++){
		buffer[i] = 0x55; //170, 10101010
	}
	for (int i=188; i < 200; i++) {
		buffer[i] = 0xFF;
	}
}

//same as a hsync_line, but every 2nd bit 
//must be 1

void generate_vsync_scan(uint8_t *buffer) {
	generate_hsync_scan(buffer);
	for (int i = 0; i < 200; i++){
		if (buffer[i] ==0xFF)
			buffer[i] = 0xAA;
		if (buffer[i] == 0x55)
			buffer[i] = 0x00;
	}
}
