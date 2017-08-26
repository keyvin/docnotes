	
	.code16
	.section .text
	.globl _start
_start:
	// clear registers
	xor %ax, %ax
	xor %bx, %bx
	xor %cx, %cx
	xor %dx, %dx
	// clear data segments
	mov %ax, %ds
	mov %ax, %es
	mov %ax, %fs
	mov %ax, %gs
	// set stack segment and stack pointer
	// kernel is loaded at 0x10000 so the top is 0xfffc
	mov %ax, %ss
	mov $0xfffc, %sp
	// move message to source index register
	lea data_message, %si
	call bootloader_print
	pushf 
	// halt cpu
	cli


	hlt

bootloader_print:
	push %ax
	push %bx
	.bootloader_print_byte:
	lodsb
	cmp $0, %al
	je .bootloader_print_end
	mov $0x0e, %ah
	mov $0x00, %bh
	mov $0x07, %bl
	int $0x10
	jmp .bootloader_print_byte
	.bootloader_print_end:
	pop %bx
	pop %ax
	ret

data_message:
	.ascii "hello world\n"
interrupt_msg:
	.ascii "interrupts disabled"
disable_ints:	
	.dw 0xE0
