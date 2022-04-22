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
	float freq = 10000000.0;
	float div = (float)clock_get_hz(clk_sys) / freq;
	PIO pio = pio1;
	uint offset_z80io = pio_add_program(pio, &z80io_program);
	uint sm_z80io = pio_claim_unused_sm(pio, true);	
	
	
	//gpio_set_dir(13,0);
	gpio_init(12);
	gpio_init(11);
	gpio_init(10);
	gpio_set_dir(10,GPIO_OUT);	
	gpio_set_dir(11,GPIO_IN);
	gpio_put(10,1);
	gpio_set_dir(12,GPIO_IN);
	gpio_pull_up(11);
	gpio_pull_down(12);
	//for (int i = 0; i < 8; i++) gpio_set_dir(14+i,0);
	z80io_init(pio, sm_z80io, offset_z80io, div);
	pio_sm_set_enabled(pio, sm_z80io, true);
	uint position = 0;
	printf("entering loop\n");
	unsigned int loop =0;

	uint32_t o = 0;
	uint32_t r1,r2,r3,r4;
	uint32_t count = 0;
	uint8_t regs[4] = {0,0,0,0};
	uint8_t base = 0;
	while (1) {
		if(pio_interrupt_get(pio, 5)){

		  r1 = pio_sm_get(pio,sm_z80io);
		  base = (uint8_t)((r1 & 0x0000FF00) >> 8);
		  regs[base] = (uint8_t) r1 & 0x000000FF; 
		  printf("(out) %d, base - %d, val - %d, count - %d\r\n", r1, base, regs[base],r4++ );
		  pio_interrupt_clear(pio, 5);
				
		}
		if(pio_interrupt_get(pio, 6)) {	
		  pio_sm_get(pio,sm_z80io);		  
		  r1 = pio_sm_get(pio,sm_z80io);
		  base = (uint8_t)((r1 & 0x0000FF00) >> 8);		  
		  printf("(in) %d, base - %d, val - %d, count - %d\r\n", r1, base, regs[base],r4++ );
		  r1 = regs[base];
		  r2 = r1 << 24 | r1 << 16 | r1 <<8 | r1;		  
		  pio_sm_put(pio, sm_z80io, r2);
		  pio_interrupt_clear(pio,6);				
		}
	}

}
