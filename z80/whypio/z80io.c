#include <stdio.h>
#include  "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/gpio.h"
#include "hardware/clocks.h"
#include "hardware/dma.h"
#include "hardware/structs/bus_ctrl.h"
//#include "pico/multicore.h"
#include "z80io.pio.h"


int main() {
	stdio_init_all();
	float freq = 50000000.0;
	float div = (float)clock_get_hz(clk_sys) / freq;
	PIO pio = pio1;
	uint offset_z80io = pio_add_program(pio, &z80io_program);
	uint sm_z80io = pio_claim_unused_sm(pio, true);	
	z80io_init(pio, sm_z80io, offset_z80io, div);
	
	//gpio_set_dir(13,0);
	gpio_init(12);
	gpio_init(13);
	gpio_init(11);
	gpio_set_dir(12,GPIO_OUT);	
	gpio_set_dir(13,GPIO_IN);
	gpio_put(12,1);
	gpio_pull_up(13);
	gpio_set_dir(11,GPIO_IN);
	//for (int i = 0; i < 8; i++) gpio_set_dir(14+i,0);
	pio_sm_set_enabled(pio, sm_z80io, true);
	uint position = 0;
	printf("entering loop\n");
	unsigned int loop =0;
	uint32_t a;
	uint32_t o = 0;
	uint32_t f =0;
	uint32_t count = 0;
	while (1) {
		if(!pio_sm_is_rx_fifo_empty(pio, sm_z80io)){
		a =f = o = pio_sm_get(pio,sm_z80io);
		
		o = a&0x00001100;
		f = a&0x000000ff;
		if (o==0x00001100)printf("width set %d\r\n", a);
		if (o==0x00001100)printf ("truncated 32 is %d\nRegular is %d\r\n", (uint8_t) f, f);
		if (o==0x00000100)printf("x set\r\n");
		if (o==0x00001000)printf("y set\r\n");
		if (o==0x0000000) count++;
		if (count%25 == 0) printf("25 writes\r\n");
		//printf("recieved %d\r\n",o);

		
		position++;
		}
		if (position == 19200)position=0;

	}

		
	
}