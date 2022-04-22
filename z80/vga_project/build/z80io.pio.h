// -------------------------------------------------- //
// This file is autogenerated by pioasm; do not edit! //
// -------------------------------------------------- //

#pragma once

#if !PICO_NO_HARDWARE
#include "hardware/pio.h"
#endif

// ----- //
// z80io //
// ----- //

#define z80io_wrap_target 0
#define z80io_wrap 5

static const uint16_t z80io_program_instructions[] = {
            //     .wrap_target
    0xa442, //  0: nop                    side 0 [4] 
    0x220d, //  1: wait   0 gpio, 13      side 0 [2] 
    0x400e, //  2: in     pins, 14        side 0     
    0x9020, //  3: push   block           side 1     
    0xb042, //  4: nop                    side 1     
    0x328d, //  5: wait   1 gpio, 13      side 1 [2] 
            //     .wrap
};

#if !PICO_NO_HARDWARE
static const struct pio_program z80io_program = {
    .instructions = z80io_program_instructions,
    .length = 6,
    .origin = -1,
};

static inline pio_sm_config z80io_program_get_default_config(uint offset) {
    pio_sm_config c = pio_get_default_sm_config();
    sm_config_set_wrap(&c, offset + z80io_wrap_target, offset + z80io_wrap);
    sm_config_set_sideset(&c, 1, false, false);
    return c;
}

static inline void z80io_init(PIO pio, uint sm, uint offset, float freq) {
	pio_sm_config c = z80io_program_get_default_config(offset);
	for (int i=0;i<10;i++) pio_gpio_init(pio, 14+i);
	pio_gpio_init(pio, 26);
	pio_sm_set_consecutive_pindirs(pio, sm, 14, 10, false);
	sm_config_set_out_pins(&c, 14, 8);
	sm_config_set_clkdiv(&c, freq);
	sm_config_set_out_shift(&c, true, true, 8);
	sm_config_set_in_shift(&c, false, true, 32);
	sm_config_set_sideset_pins(&c, 12);
	sm_config_set_sideset(&c, 1, false, false);
	sm_config_set_in_pins(&c, 14);
	sm_config_set_jmp_pin(&c, 11);
	pio_sm_init(pio, sm, offset, &c);
}

#endif
