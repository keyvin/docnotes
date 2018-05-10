/* Declare constants for the multiboot header. */
.set ALIGN,    1<<0             /* align loaded modules on page boundaries */
.set MEMINFO,  1<<1             /* provide memory map */
.set FLAGS,    ALIGN | MEMINFO  /* this is the Multiboot 'flag' field */
.set MAGIC,    0x1BADB002       /* 'magic number' lets bootloader find the header */
.set CHECKSUM, -(MAGIC + FLAGS) /* checksum of above, to prove we are multiboot */

.section .multiboot
.align 4
.long MAGIC
.long FLAGS
.long CHECKSUM
.section .bss
.align 16
stack_bottom:
.skip 16384 # 16 KiB
stack_top:
	.byte 0 /*insert space*/

	
.section .gdt
	
	
	

.section .text
.global _start
.type _start, @function
_start:
	
	lgdt (gdtr)
	ljmp $0x08, $here
	jmp here
here:	
	mov $0x10, %ax
	mov %ax, %ds
	mov %ax, %es
	mov %ax, %fs
	mov %ax, %gs
	mov %ax, %ss
	mov seven, %eax
	
	mov $stack_top, %esp
	call kernel_main

	cli
1:	hlt
	jmp 1b

	

GDT:	
	
	.long 0	
	.long 0
	
	.short 0xffff
	.short 0
	.byte 0
	.byte 0x9a
	.byte 0b1100111
	.byte 0

	.short 0xffff
	.short 0
	.byte 0
	.byte 0x92
	.byte 0b1100111
	.byte 0
end_of_gdt:

	.align 8
gdtr:	
	.short 23
	.long GDT


.section .worthless
	.short 5
	.short 6
seven:	
	.short 7

	
	
//.size _start, . - _start
