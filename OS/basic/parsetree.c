//#include <stdlib.h>
//#include <stdio.h>
//#include <math.h>
#include "parsetree.h"
//#include <string.h>
#include "stdcall.h"
/*I may need to define some error codes*/
/*They could be stored in the int value of an undefined node*/

int calcTree(evaltree *currnode, var *varlist){
  var *getvar;
  /*descend left branch*/
  /*this is a hack to fix something happening in the parser*/
  

  if (currnode->left){
    calcTree(currnode->left, varlist);
  }

  /*descend right branch*/
  if (currnode->right){
    calcTree(currnode->right, varlist);
  }
  /*A variable containing element of the tree will always be a leaf*/
  //or a string...
  /*look up value and set it. */
  if (currnode->varname[0]!='\0'){
    getvar= getVar(varlist, currnode->varname);
    if (getvar){
      if (getvar->val.type == str){
	currnode->result.value.s = (char *) my_malloc(sizeof(char)*strlen(getvar->val.value.s));
	strcpy(currnode->result.value.s, getvar->val.value.s);
      }
      else
	currnode->result = getvar->val;
      
    }
    else {
	currnode->result.value.i = currnode->val.value.i;
	currnode->result.type = integer;
    }
    return 0;
  }
  //A string
  // if (currnode->val.type == str){
  //  currnode->result.type = str;
  //  currnode->result.value.s = currnode->val.value.s;
  //  return 0;
  //}
  vartype ltype, rtype;
  varval *lval;
  varval *rval;
    
  if (currnode->left){
    ltype = currnode->left->result.type; 
    lval = &(currnode->left->result.value);
  }
  if (currnode->right){
    rtype = currnode->right->result.type;
    rval = &(currnode->right->result.value);
  }
  
  switch (currnode->operator){
    /*leaf node, set result as value*/
    //TODO - This is a hack, needs to be properly fixed in parser
    case'\0':
      if (currnode->left){
	currnode->result = currnode->left->result;
	currnode->left->val.value.s = NULL;
	currnode->left->result.value.s = NULL;
      }
      else if (currnode->right){
	currnode->result = currnode->right->result;
	currnode->right->val.value.s = NULL;
	currnode->right->result.value.s = NULL;
      }
      else {
	currnode->result = currnode->val;
	currnode->val.value.s = NULL;
      }
	
      break;
   /*non leafs. Perform appropriate calculation of children based on type*/
    case '+':
      if (ltype == integer && rtype == integer){
	currnode->result.value.i = lval->i + rval->i;
	currnode->result.type = integer;
      }
      else if (ltype == integer && rtype == floating){
	currnode->result.type = integer;
	currnode->result.value.i = lval->i + (int) rval->f;
      }
      else if (ltype == floating && rtype == integer){
	currnode->result.type = integer;
	currnode->result.value.i = (int) lval->f + rval->i;
      }
      else if (ltype == floating && rtype == floating){
	currnode->result.type = floating;
	currnode->result.value.f = lval->f + rval->f;
      }
      //todo - wrong.
      else if (ltype == str && rtype == str){
	currnode->result.value.s = my_malloc(strlen(lval->s)+strlen(rval->s)+1);
	strcpy(currnode->result.value.s, lval->s);
	strcat(currnode->result.value.s, rval->s);
      }
      else {
	currnode->result.value.i = 0;
	currnode->result.type = undefined;
      }
      break;
    case '/':
      if (ltype == integer && rtype == integer){
	currnode->result.value.i = lval->i / rval->i;
	currnode->result.type = integer;
      }
      else if (ltype == integer && rtype == floating){
	currnode->result.type = integer;
	currnode->result.value.i = lval->i / (int) rval->f;
      }
      else if (ltype == floating && rtype == integer){
	currnode->result.type = integer;
	currnode->result.value.i = (int) lval->f / rval->i;
      }
      else if (ltype == floating && rtype == floating){
	currnode->result.type = floating;
	currnode->result.value.f = lval->f / rval->f;
      }
      else {
	currnode->result.value.i = 0;
	currnode->result.type = undefined;
      }

      break;
    case '-':
      if (ltype == integer && rtype == integer){
	currnode->result.value.i = lval->i - rval->i;
	currnode->result.type = integer;
      }
      else if (ltype == integer && rtype == floating){
	currnode->result.type = integer;
	currnode->result.value.i = lval->i - (int) rval->f;
      }
      else if (ltype == floating && rtype == integer){
	currnode->result.type = integer;
	currnode->result.value.i = (int) lval->f - rval->i;
      }
      else if (ltype == floating && rtype == floating){
	currnode->result.type = floating;
	currnode->result.value.f = lval->f - rval->f;
      }
      else {
	currnode->result.value.i = 0;
	currnode->result.type = undefined;
      }
      break;
    case '*':
      if (ltype == integer && rtype == integer){
	currnode->result.value.i = lval->i * rval->i;
	currnode->result.type = integer;
      }
      else if (ltype == integer && rtype == floating){
	currnode->result.type = integer;
	currnode->result.value.i = lval->i * (int) rval->f;
      }
      else if (ltype == floating && rtype == integer){
	currnode->result.type = integer;
	currnode->result.value.i = (int) lval->f * rval->i;
      }
      else if (ltype == floating && rtype == floating){
	currnode->result.type = floating;
	currnode->result.value.f = lval->f * rval->f;
      }
      else {
	currnode->result.value.i = 0;
	currnode->result.type = undefined;
      }

      break;
    case '&':
      currnode->result.value.i = (currnode->left->result.value.i && currnode->right->result.value.i) ? 1 :0;
      currnode->result.type = integer;
      break;
    case '|':
      currnode->result.value.i = (currnode->left->result.value.i || currnode->right->result.value.i) ?1 :0;
      currnode->result.type = integer;
      break;
    case '<':
      currnode->result.value.i = (lval->i < rval->i) ? 1:0;
      currnode->result.type = integer;
      break;
    case '>':
      currnode->result.value.i = (lval->i > rval->i) ?1:0;
      currnode->result.type = integer;
      break;
    case '=':
      currnode->result.value.i = (lval->i == rval->i) ?1:0;
      currnode->result.type = integer;
      break;
    case '^':
      //currnode->result.value.i = pow(lval->i, rval->i);
      currnode->result.type = integer;
      break;
  }
 
 // printf ("result so far: %d\n", currnode->result);
  return 0;
}



evaltree * genNewNode() {
  evaltree *ptr = (evaltree *) my_malloc(sizeof(evaltree));
  ptr->val.type = integer;
  ptr->val.value.i = 0;
  ptr->result.value.i = 0;
  ptr->operator = '\0';
  ptr->varname[0] = '\0';
  ptr->left = NULL;
  ptr->right = NULL;
  return ptr;
}

void freeTree(evaltree *currnode){
  if (currnode->left)
    freeTree(currnode->left);
  if (currnode->right)
    freeTree(currnode->right);
  if (currnode) {
    if (currnode->val.type == str && currnode->val.value.s){
      my_free(currnode->val.value.s);
      
    }
    if (currnode->result.type == str && currnode->result.value.s)
      if (currnode->val.value.s != currnode->result.value.s)
	my_free(currnode->result.value.s);
    my_free(currnode);
  }
  return;
}
