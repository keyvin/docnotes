#ifndef LIST
#define LIST 1
#include "varlist.h"

typedef struct LINE {
  unsigned int lineno;
  char instruction[150];
  struct LINE *prev;
  struct LINE *next;
} line;


line *executeLine(line *, var *);
line *insertLine(line *, line *);
line *newLine(char *);
void freeLineList(line *);
void printList(line *);
#endif
