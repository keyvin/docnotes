OUTPUT_FORMAT("binary")
ENTRY(_start)
SECTIONS
{
     . = 0x7c00;
     .text : AT(0x7c00) {

     *(.text)
			}
     .sig : AT(0x7dfe) {
      SHORT(0xaa55)

      }

}
