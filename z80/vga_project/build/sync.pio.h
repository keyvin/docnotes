// -------------------------------------------------- //
// This file is autogenerated by pioasm; do not edit! //
// -------------------------------------------------- //

#pragma once

#if !PICO_NO_HARDWARE
#include "hardware/pio.h"
#endif

// ---- //
// sync //
// ---- //

#define sync_wrap_target 2
#define sync_wrap 4

static const uint16_t sync_program_instructions[] = {
    0xc047, //  0: irq    clear 7                    
    0xa042, //  1: nop                               
            //     .wrap_target
    0x6002, //  2: out    pins, 2                    
    0xa042, //  3: nop                               
    0xa042, //  4: nop                               
            //     .wrap
};

#if !PICO_NO_HARDWARE
static const struct pio_program sync_program = {
    .instructions = sync_program_instructions,
    .length = 5,
    .origin = -1,
};

static inline pio_sm_config sync_program_get_default_config(uint offset) {
    pio_sm_config c = pio_get_default_sm_config();
    sm_config_set_wrap(&c, offset + sync_wrap_target, offset + sync_wrap);
    return c;
}

static inline void sync_program_init(PIO pio, uint sm, uint offset, uint pin, float freq) {
        pio_sm_config c = sync_program_get_default_config(offset);
        //config, base, num
        for (int i=0;i<2;i++) {pio_gpio_init(pio, pin+i);}
        pio_sm_set_consecutive_pindirs(pio, sm, pin, 2, true);
        sm_config_set_out_pins(&c, pin, 2);
        sm_config_set_clkdiv(&c, freq);
	sm_config_set_out_shift(&c, false, true, 8);
	//connect pins to this pio
        //init on pio
        pio_sm_init(pio, sm, offset, &c);
        //start
}

#endif
