#ifndef VARLIST
#define VARLIST 1
#define MAX_VAR_LENGTH 20

typedef enum {str, integer, floating, undefined} vartype;

typedef union VAR_VAL {
  int i;
  float f;
  char *s;
} varval;

typedef struct VARIABLE {
  vartype type;
  varval value;
} value;
  

typedef struct VAR{
  char varname[MAX_VAR_LENGTH];
  value val;
  struct VAR *next;
} var;


var * createVar();
var * getVar(var *, char *);
void setVar(var *, char*, value);
void freeVarlist(var *);
#endif
