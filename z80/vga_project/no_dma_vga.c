#include  "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/gpio.h"
#include "hardware/clocks.h"
#include "rgb.pio.h"
#include "sync.pio.h"

//Goal is to create functions that 
//create buffers with the timing pixels
//embedded. 

//Ex. a 640x480@60hz has 800 pixels per line
//640 visible (RGB values, but no H&V sync)
//16 Front porch, 96 sync pulse, 48 back porch
//after 480 of these lines, we have a vsync line
//10 Front porch, 2 sync pulse, 33 back porch

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
uint8_t RGB_buffer[800]; //8bpp
uint8_t Vblank[800];   //8bpp, 0s
uint8_t Hsync_buffer[200]; //2bpp(HVHVHVHV)
uint8_t Vsync_buffer[200]; //2bpp 


void generate_rgb_scan(uint8_t *);
void generate_vblank_rgb(uint8_t *);
void generate_hsync_scan(uint8_t *);
void generate_vsync_scan(uint8_t *);

int main(){
//our output is 480 lines of rgb and hsync.
//10 lines of vblank and hsync
//2 lines of vblank and vsync
//33 lines of vblank and hsync 
	generate_rgb_scan(RGB_buffer);
	generate_vblank_rgb(Vblank);
	generate_hsync_scan(Hsync_buffer);
	generate_vsync_scan(Vsync_buffer);	
	PIO pio = pio0;
	float freq = 25175000.0;
	float div = (float)clock_get_hz(clk_sys) / freq;
	uint offset_rgb = pio_add_program(pio, &rgb_program);
	uint offset_sync = pio_add_program(pio, &sync_program);
	uint sm_sync = pio_claim_unused_sm(pio, true);
	uint sm_rgb = pio_claim_unused_sm(pio, true);
	//must be started in this order
	rgb_program_init(pio, sm_rgb, offset_rgb, 0, div);
	sync_program_init(pio, sm_sync, offset_sync, 10, div);
	//make sure fifos have something in them
	uint32_t blank = 0;
	uint8_t blank8 = 0;
	//to keep in sync, rgb needs 4x the data (2 bits per 8 bits)  
	pio_sm_put(pio, sm_rgb, blank);
	pio_sm_put(pio, sm_sync, blank8);
	//rgb first, sync second.
	pio_sm_set_enabled(pio, sm_rgb, true);
	pio_sm_set_enabled(pio, sm_sync, true);
	uint16_t scanline = 0;
	uint16_t pixel = 0;
	uint32_t *rgb;
	uint8_t *sync;	
	uint8_t flip =0;
	while (1) {
		if (scanline <  480) {
			rgb = (uint32_t *) RGB_buffer;
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
                unsigned int f = 0;
		while (pixel < 200){    //800/4
			pio_sm_put_blocking(pio, sm_sync, sync[pixel]);
			pio_sm_put(pio, sm_rgb, rgb[pixel]); 
			pixel++;

                }
		pixel = 0;
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