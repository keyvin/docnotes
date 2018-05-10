export PATH=/home/keyvin/opt/cross/bin:$PATH
i686-elf-gcc -c boot.s -o boot.o 
i686-elf-gcc -c kernel.c -o kernel.o -std=gnu99 -ffreestanding -O2 -Wall 
i686-elf-gcc -c keyboard.c -o keyboard.o -std=gnu99 -ffreestanding -O2 -Wall
for i in $(ls ./basic/*.c); do i686-elf-gcc -c $i -o $i.o -std=gnu99 -ffreestanding -O2 -Wall; done
i686-elf-gcc -c keyboard.c -o keyboard.o -std=gnu99 -ffreestanding -O2 -Wall -Wextra
i686-elf-gcc -T kern.ld -o os.bin -ffreestanding -O2 -nostdlib boot.o kernel.o keyboard.o ./basic/*.o  -lgcc
rm ./iso/boot/os.bin
cp os.bin ./iso/boot/
grub-mkrescue -o mk.iso iso
qemu-system-i386 -kernel os.bin
