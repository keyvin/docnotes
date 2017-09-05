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

/*tree structure.*/



/*creates an empty node*/

/*parses the input and builds the calculation tree*/

/*calculates value of tree*/


int basic(){
  char buffer[201];
  char tmpvarname[20];
 
  char *startpos = buffer;
  line *currinstruction = NULL;
  line *list = NULL;
  line *tmp = NULL;
  int setvar=0;
  char *eof = NULL;

  // while (1){
  // startpos = buffer;
  // setvar=0;
    //eof = fgets(buffer, 100, stdin);
    //if (!eof){
    //       printf("EOF Encountered. Exiting\n");
    //  return 0;
    //}
    //if (strlen(buffer)==1)
    //  continue;
    //buffer[strlen(buffer)-1]= '\0';
    //if (!strncmp("EXEC", buffer, 4)){
      //printf("exec encountered\n");
      // executor(list, NULL);
      //}
    //else{
     //tmp = newLine(buffer);
     //list = insertLine(list, tmp);
  list = insertLine(list, newLine("10 PRINT 11+11\n"));
  list = insertLine(list, newLine("20 SET B=3+3\n"));
  list = insertLine(list, newLine("30 PRINT B+3\n"));
      executor(list, NULL);

      //printList(list);
      //    }
// }    
  return 0;
}


    

  




