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
	gpio_init(11);
	gpio_init(10);
	gpio_set_dir(10,GPIO_OUT);	
	gpio_set_dir(11,GPIO_IN);
	gpio_put(10,1);
	gpio_set_dir(12,GPIO_IN);
//	gpio_pull_up(11);
//	gpio_pull_up(12);
	//for (int i = 0; i < 8; i++) gpio_set_dir(14+i,0);
	pio_sm_set_enabled(pio, sm_z80io, true);
	uint position = 0;
	printf("entering loop\n");
	unsigned int loop =0;
	uint32_t a;
	uint32_t o = 0;
	uint32_t f =0;
	uint32_t count = 0;
	uint32_t r1;
	uint32_t r2;
	uint32_t r3=0;
	uint32_t r4=0;
	pio_sm_clear_fifos(pio,sm_z80io);
	while (1) {
		if(pio_interrupt_get(pio, 5)){
				o = a&0x00001100;
				f = a&0x000000ff;
				printf("(out) %u, %d\r\n", r1 = pio_sm_get(pio,sm_z80io), r4++);
				pio_interrupt_clear(pio, 5);
		}
		if(pio_interrupt_get(pio, 6)) {	
				o = a&0x00001100;
				f = a&0x000000ff;
				pio_sm_get(pio,sm_z80io);
				pio_sm_clear_fifos(pio,sm_z80io);
				printf("(inp) %d %d\r\n",r1, r3++);
				r2 = r1 << 24 | r1 << 16 | r1 <<8 | r1;
				pio_sm_put(pio, sm_z80io, r2);
				pio_interrupt_clear(pio,6);

				

			//printf("recieved %d\r\n",o);
			//printf("interrupt cleared\n");
		}
	}

}
