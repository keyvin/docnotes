export PATH=/home/sysv/opt/cross/bin:$PATH
i686-elf-gcc -c kernel.c -o kernel.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra
i686-elf-gcc -c keyboard.c -o keyboard.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra
i686-elf-gcc -T kern.ld -o myos.bin -ffreestanding -O2 -nostdlib boot.o kernel.o keyboard.o  -lgcc
qemu-system-i386 -kernel myos.bin
