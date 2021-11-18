cmake_minimum_required(VERSION 3.13)

include (pico_sdk_import.cmake)
project (simple_vga C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(SIMPLE_VGA_PATH ${PROJECT_SOURCE_DIR})

pico_sdk_init()
add_executable(simple_vga)
pico_generate_pio_header(simple_vga ${CMAKE_CURRENT_LIST_DIR}/sync.pio) 
pico_generate_pio_header(simple_vga ${CMAKE_CURRENT_LIST_DIR}/rgb.pio)
pico_generate_pio_header(simple_vga ${CMAKE_CURRENT_LIST_DIR}/z80io.pio)
target_sources(simple_vga PRIVATE vga.c)

target_link_libraries(simple_vga PRIVATE
        pico_stdlib
        hardware_pio
	hardware_dma
	pico_multicore
)

pico_add_extra_outputs(simple_vga)


