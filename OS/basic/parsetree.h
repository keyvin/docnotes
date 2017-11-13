#ifndef PARSETREE
#define PARSETREE 1
#include "varlist.h"

typedef struct EVALTREE {
  value val;
  value result;

  char operator;
  char varname[MAX_VAR_LENGTH];
  struct EVALTREE *left;
  struct EVALTREE *right;
} evaltree;


int calcTree(evaltree *, var *);
void freeTree(evaltree *);
evaltree *genNewNode();
#endif
