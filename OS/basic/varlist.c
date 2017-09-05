#include "varlist.h"
//#include <stdlib.h>
//#include <string.h>
#include "stdcall.h"


var * createVar(){
  var *newvar = (var *) my_malloc(sizeof(var));
  memset(newvar->varname, '\0', MAX_VAR_LENGTH);
  newvar->val.value.i = 0;
  newvar->val.type = integer;
  newvar->next = NULL;
  return newvar;
}

var * getVar(var *head, char *varname){  
  var *list = NULL;
  if (!head)
    return NULL;
  for (list=head; list!=NULL; list=list->next){
    if (strcmp(list->varname, varname)==0)
      return list;
  }
  return NULL;
}

//if first element of list is empty, assign a value to first element
void setVar(var *head, char *varname, value val){
  var * existing = NULL;
  
  if (head->varname[0]=='\0'){
    strcpy( head->varname, varname );

    if (val.type == str){
      head->val.value.s = (char *) my_malloc(strlen(val.value.s) + 1);
      strcpy(head->val.value.s, val.value.s); 
      head->val.type = str;
    }
    else
      head->val = val;
      
  
    head->next = NULL;
    return;
  }

  if (existing = getVar(head, varname)){
    if (existing->val.type == str){
      if (existing->val.value.s){
	my_free(existing->val.value.s);
      }
    }
    existing->val = val;
    return;
  }
  
  existing = createVar();
  strcpy( existing->varname, varname );

  if (val.type == str){
    existing->val.value.s = (char *) my_malloc(strlen(val.value.s)+1);
    strcpy(existing->val.value.s, val.value.s);
    existing->val.type = str;
  }
  else
    existing->val = val;
  existing->next = NULL;
  while (head->next != NULL){
    head = head->next;
  }
  head->next = existing;
  return;
}

void freeVarList(var *head){
  var *tmp= NULL;
  while (head!=NULL)
  {
    tmp = head->next;
    if (head->val.type == str && head->val.value.s)
      my_free(head->val.value.s);
    my_free(head);
    head = tmp;
  }
  return;
}
      
  
  
