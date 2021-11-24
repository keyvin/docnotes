#include <stdio.h>
#include  "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/gpio.h"
#include "hardware/clocks.h"
#include "hardware/dma.h"
#include "hardware/structs/bus_ctrl.h"
#include "pico/multicore.h"
#include "rgb.pio.h"
#include "sync.pio.h"
#include "z80io.pio.h"
#define X_RES 160
#define Y_RES 120

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
uint8_t RGB_buffer[2][800]; //8bpp
uint8_t Vblank[800];   //8bpp, 0s
uint8_t Hsync_buffer[200]; //2bpp(HVHVHVHV)
uint8_t Vsync_buffer[200]; //2bpp 

uint8_t background[19200];

void generate_rgb_scan(uint8_t *);
void generate_vblank_rgb(uint8_t *);
void generate_hsync_scan(uint8_t *);
void generate_vsync_scan(uint8_t *);

void fill_background() {
	for (int i =0; i < 120; i++)
		for (int j = 0;  j < 160; j++) {
			background[(i*160)+j] = j;
		}
}

void fill_scan(uint8_t *buffer, int line) {
	int start = line*160;
	int s = 0;
	for (int sweep = 0; sweep < 160; sweep++) {
		s = sweep*4;	
		buffer[s] = background[start+sweep];	
		buffer[s+1] = background[start+sweep];	
		buffer[s+2] = background[start+sweep];	
		buffer[s+3] = background[start+sweep];	
	}
}

void z80io_core_entry() {
	float freq = 50000000.0;
	float div = (float)clock_get_hz(clk_sys) / freq;
	PIO pio = pio1;
	uint offset_z80io = pio_add_program(pio, &z80io_program);
	uint sm_z80io = pio_claim_unused_sm(pio, true);	
	z80io_init(pio, sm_z80io, offset_z80io, div);
	pio_sm_set_enabled(pio, sm_z80io, true);
	gpio_init(11);
	gpio_init(12);
	gpio_init(13);
	gpio_set_dir(11,GPIO_IN);
	gpio_set_dir(13,GPIO_IN);
	gpio_set_dir(12,GPIO_OUT);
	gpio_put(12,1);
	//gpio_pull_up(13);
	//gpio_put(12,1);
	//gpio_set_dir(11,0);

	uint32_t position = 0;
	uint32_t io = 0;
	uint16_t regs = 0;
	uint8_t row = X_RES;
	uint8_t col = Y_RES;
	uint8_t extent = 0;
	uint8_t x = 0;
	uint8_t y = 0;
	uint8_t old =0;
	uint8_t new = 0;
	//bit fields for the registers are due to
	//3 pin gap on pi pico (rp2040) - 
	while (1) {
		if(!pio_sm_is_rx_fifo_empty(pio, sm_z80io)){
			io = pio_sm_get(pio, sm_z80io) &0x0000011FF;
			//are register pins set?
			regs = (uint16_t) io &0x1100;
			if (regs == 0) {
				if ((((uint8_t) io)) != old){
						printf("new %d\n", (uint8_t) io);
						old = (uint8_t) io;
				}
				if (extent == 0x25) {
				 background[ (y*X_RES)+x] = (uint8_t)io;
				 x++;
				 if (x  >= col+extent){
					x =col;
					y++;
				 }
				 if (y >= row+extent) {
					y = row;
				 }
				}
				else {				
				 background[position] = (uint8_t)io;	
				 position++;
				 if (position == 19200){position=0 ;}				 
				}
			}
			//row address set
			else if (regs ==  0x0100){
				//row start
				//printf ("setting x,col: %d\r\n", io&0x000000ff);
				x = col = (uint8_t) (io) ;
				y = row;
				if (col >= X_RES)
					x =col =0;
					

			}
			//column address set
			else if (regs == 0x1000) {
				//printf ("setting y,row: %d\r\n", io&0x000000ff);
				y = row = (uint8_t) (io) ;
				x = col;
				if (row >= Y_RES)
					y = row =0;
			}
			//width (square for now)
			else if (regs == 0x01100) {
				uint8_t ox = extent;
				extent = ((uint8_t) io);
		//		printf ("setting extent: %d\r\n", io&0x000000ff);
				if (col + extent > X_RES)
					extent = 0;
				if (row + extent > Y_RES)
					extent = 0;
				if (extent ==0)	{ //switch to absolute 
					for (uint i = 0; i < 19200/4; i++) *(((uint32_t *) background) +i) = 0;
					position =  0;
				}
				x = col;
				y = row;
			}
		}

		
		
	}

		
	
	
}

int main(){
//our output is 480 lines of rgb and hsync.
//10 lines of vblank and hsync
//2 lines of vblank and vsync
//33 lines of vblank and hsync 
	//stdio_init_all();
	generate_rgb_scan(RGB_buffer[0]);
	generate_rgb_scan(RGB_buffer[1]);
	generate_vblank_rgb(Vblank);
	generate_hsync_scan(Hsync_buffer);
	generate_vsync_scan(Vsync_buffer);	
	fill_background();
	fill_scan(RGB_buffer[0],0);
	fill_scan(RGB_buffer[1],0);
	PIO pio = pio0;
	float freq = 25175000.0;
	float div = (float)clock_get_hz(clk_sys) / freq;
	uint offset_rgb = pio_add_program(pio, &rgb_program);
	uint offset_sync = pio_add_program(pio, &sync_program);
	uint sm_sync = pio_claim_unused_sm(pio, true);
	uint sm_rgb = pio_claim_unused_sm(pio, true);
	//must be started in this order
	rgb_program_init(pio, sm_rgb, offset_rgb, 0, div);
	sync_program_init(pio, sm_sync, offset_sync, 9, div);
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
	pio_sm_set_enabled(pio, sm_rgb, true);
	pio_sm_set_enabled(pio, sm_sync, true);
	multicore_launch_core1(z80io_core_entry);

	while (1) {
		if (scanline <  480) {
			if (flip==1)flip=0;
			else if (flip==0)flip=1;
			rgb = (uint32_t *) RGB_buffer[flip];
			
			sync = Hsync_buffer;
		}

		else if (scanline  < 490) {
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
			continue;
		}
		//we could alternate buffers, assign blocks, etc. 
		dma_channel_set_read_addr(rgb_dma_chan, rgb, true);
		dma_channel_set_read_addr(sync_dma_chan, sync, true);
		//fill the buffer for the flip
		fill_scan(RGB_buffer[((flip+1)%2)], (int)scanline/4);
		dma_channel_wait_for_finish_blocking(sync_dma_chan);
		scanline++;

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
