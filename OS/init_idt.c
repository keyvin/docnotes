
#include <stdint.h>
#define ENTRIES 256

struct idtr {
  uint16_t limit;
  uintptr_t base;
} __attribute__((packed));

typedef struct IDTDescr {
   uint16_t offset_1; // offset bits 0..15
   uint16_t selector; // a code segment selector in GDT or LDT
   uint8_t zero;      // unused, set to 0
   uint8_t type_attr; // type and attributes, see below
   uint16_t offset_2; // offset bits 16..31
} __attribute__((packed)) idt_entry;


static idt_entry idt_table[256];


struct interrupt_frame;


//selector will always be 0x08 for the code segment - defined in boot.s

 
__attribute__((interrupt)) void generic_handler(struct interrupt_frame *frame)
{
    /* do something */
  
  terminal_writestring("\ninterrupt occured\n");
  //need to remap pic interrupts
  //__asm__("movb $0x20, %al");
  //__asm__("outb %al, $0x20");  
  return;
}


void load_idt()
{
  struct idtr rec;
  rec.limit = 8*256-1;
  rec.base = idt_table;

  __asm__("lidt %0" :: "m"(rec));
  return;
}

void fill_table() {
  idt_entry to_fill;
  uint32_t ptr = (uint32_t) (void *) generic_handler;
  uint32_t tmp = ptr & 0x0000ffff; //lower
  uint16_t low = (uint16_t) tmp;
  tmp = ptr & 0xffff0000;
  tmp = tmp >> 16;
  uint16_t high = (uint16_t) tmp;
  
  to_fill.offset_1 = low;
  to_fill.selector = 0x08;
  to_fill.zero = 0;
  to_fill.type_attr = 0x8E;
  to_fill.offset_2 = high;
        
  for (int a = 0; a < ENTRIES; a++)
  {
    idt_table[a] = to_fill;
  }
  return;
}






