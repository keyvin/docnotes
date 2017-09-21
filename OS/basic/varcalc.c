//#include <stdlib.h>
//#include <stdio.h>
//#include <string.h>
//#include <ctype.h>
//#include <math.h>
#include "stdcall.h"
#include "varlist.h"
#include "line.h"
#include "parse.h"
#include "parsetree.h"
#include "executor.h"

//Define freestanding to compile with stdcall vs stdlib
#define freestanding 1
#define KB_BUFFSIZE 200
/*tree structure.*/



/*creates an empty node*/

/*parses the input and builds the calculation tree*/

/*calculates value of tree*/
inline unsigned char inportb_2(unsigned int port)
{
   unsigned char ret;
   asm volatile ("inb %%dx,%%al":"=a" (ret):"d" (port));
   return ret;
}

void get_string(char *buffer){
  char a = 0;
  char old_a = 1;
  char c = 0;
  int pos = 0;
  /* Initialize terminal interface */
  inportb_2(0x60);
  while(1){
    a = inportb_2(0x60);
    if (old_a != a ){
      old_a = a;
      c = keyboard_to_ascii(a);
      if (c){
	if (c == 0x0E){
	  c=0
	  if (pos == 0){
	    continue;
	  }	  
	  for (int i = pos; i < KB_BUFFSIZE-1; i++){ 
	    buffer[i] = buffer[i+1];
	  }
	  pos--;
	  terminal_bkspc();
	  continue;
	}

       	terminal_putchar(c);
	buffer[pos] = c;
        if (c == '\n' || c =='\r'){
	  buffer[pos] = '\0';
	  //wait for release
	  while (inportb_2(0x60) == old_a){
	  }
	  return;
	}
	pos++;
      }
    }
	  
  }
 return;
}


int basic(){
  char buffer[KB_BUFFSIZE];
  char tmpvarname[20];
 
  char *startpos = buffer;
  line *currinstruction = NULL;
  line *list = NULL;
  line *tmp = NULL;
  int setvar=0;
  char *eof = NULL;
  memset(buffer, '\0', 200);
  while (1){
    memset(buffer, '\0', 200);
    get_string(buffer);
    startpos = buffer;
    setvar=0;
    terminal_writestring("Returned\n");
    //eof = fgets(buffer, 100, stdin);
    //if (!eof){
    //       printf("EOF Encountered. Exiting\n");
    //  return 0;
    //}
    //if (strlen(buffer)==1)
    //  continue;
   buffer[strlen(buffer)]= '\0';
    if (!strncmp("EXEC", buffer, 4)){
      //printf("exec encountered\n");
      executor(list, NULL);
    }
    else if (!strncmp("LIST", buffer, 4)){
      printList(list);
    }
    else{
     tmp = newLine(buffer);
     list = insertLine(list, tmp);
     //list = insertLine(list, newLine("10 PRINT 11+11\n"));
     //list = insertLine(list, newLine("20 SET B=3+3\n"));
     //list = insertLine(list, newLine("30 PRINT B+3\n"));
     //executor(list, NULL);

      //printList(list);
    }
    }    
  return 0;
}


    

  




