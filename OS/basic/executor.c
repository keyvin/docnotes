#include "line.h"
#include "varlist.h"
#include "stdcall.h"

int executor(line *list, var *varlist){

  var *lookup = NULL;
  line *currinstruction = NULL;
  if (!varlist)
    varlist = createVar();    
  currinstruction = executeLine(list, varlist);
  while (currinstruction){
    //printf("in instruction %d \n", currinstruction->lineno);
    currinstruction = executeLine(currinstruction, varlist);
  }
  //TODO This only works for integers
  lookup = getVar(varlist, "__RETURN");
  freeVarList(varlist);
  if (!lookup)
    return 0;
  return lookup->val.value.i;
}
