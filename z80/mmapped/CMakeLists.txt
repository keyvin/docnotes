cmake_minimum_required(VERSION 3.13)

include (pico_sdk_import.cmake)
project (z80io C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(SIMPLE_VGA_PATH ${PROJECT_SOURCE_DIR})

pico_sdk_init()

add_executable(z80io)
pico_generate_pio_header(z80io ${CMAKE_CURRENT_LIST_DIR}/z80io.pio) 
target_sources(z80io PRIVATE z80io.c)

target_link_libraries(z80io PRIVATE
    pico_stdlib
    hardware_pio
	hardware_dma
	pico_multicore
)
    pico_enable_stdio_usb(z80io 1)
    pico_enable_stdio_uart(z80io 0)
pico_add_extra_outputs(z80io)


