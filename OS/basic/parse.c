//#include <stdlib.h>
//#include <stdio.h>
//#include <string.h>
//#include <math.h>
#include "parse.h"
#include "varlist.h"
#include "parsetree.h"
#include "stdcall.h"
//returns new position in the parser.
char * readVarName(char *input, char *output){
  memset(output, '\0', 0);
  while (*input ==' ')
    input++;
  while (isalpha(*input) ){
    *output = *input;
    input++;
    output++;
  }
  *output = '\0';
  return input;
}

int isoperator(char a){
  if (a=='*' || a=='/' || a=='-' || a=='+' || a=='&' || a=='|'||a=='^'||a=='>'||a=='<'||a=='='){
    return 1;
  }
  return 0;
}


int noOperator(char *pos){
  char *currchar=pos;
  /*only check to matching ) because that is the end to the recursion*/
  for (currchar; *currchar!='\0'&&*currchar!=')'; currchar++){
    if (isoperator(*currchar))
      return 0;
  }
  return 1;
}
	
char * readString(char *start, char *ret_val, int size){
  int copied = 0;
  for (start; *start != '\0' && *start !='\"' && copied < size; start++){
    *(ret_val++) = *start;
    copied++;
  }
  *ret_val = '\0';
  start++;
  return start;
}



//creates copy of string while removing all spaces
char * deSpace(char *string){
  char *buffer, *position;
  buffer = (char *) my_malloc(strlen(string));
  position = buffer;
  for (string; *string !='\0'; string++){
    if (*string != ' '){
      *(position++) = *string;
    }
  }
  *position = '\0';
  return buffer;
}

char * buildTree(char *string, evaltree *currnode, int isleftset){
  char buffer[21];
  char *buffpos = buffer;
  char *pos = NULL;
  evaltree *tmptree;
  int leftset = isleftset;
  int val=0;
  int noop=0;
  //clear buffer
  memset(buffer, sizeof(char), '\0');
  //test for valid input
  if (string == NULL) return NULL;
  //maybe this would be better as a while
  for (pos = string; *pos!='\0'; pos++){
    //if we are entering a parenthisis
    if (!leftset){
     
      if (*pos == '('){
	//printf("encountered ( on left pair, recursing\n");
	//add new node to left side, set it as current node, and recurse
	currnode->left = genNewNode();
	//still possible to set the left side
	pos = buildTree(pos+1, currnode->left, 0);
      }
      else {
	//not a parenthisis. Read value into buffer and sscanf it.
	noop = noOperator(pos);
	//printf("Value of noop is %d\n", noop);
	if (isdigit(*pos)){
	  while (isdigit(*pos)){
	    *buffpos++ = *pos++;
	  }
	  *buffpos='\0';

	  //sscanf(buffer, "%i", &val);
	  val = read_int(buffer);
	  //printf("read left val %d\n", val);
	  //create a new leaf on left side to store read value
	  if (noop){
	    currnode->val.value.i = val;
	    currnode->val.type = integer;
	    return pos;
	  }
	  currnode->left = genNewNode();
	  currnode->left->val.value.i = val;
	  currnode->left->val.type = integer;
	  buffpos=buffer;
	}
	else if (isalpha(*pos)){
	  pos = readVarName(pos, buffer);
	  //printf ("read varname %s on left side\n", buffer);
	  if (noop){
	    strcpy(currnode->varname, buffer);
	    return pos;
	  }
	  currnode->left = genNewNode();
	  strcpy(currnode->left->varname, buffer);
	}
	//TODO arbitrary magic number string size
	else if (*pos == '\"'){
	  pos++;
	  currnode->left = genNewNode();
	  currnode->left->val.type = str;
	  currnode->left->val.value.s = (char *) my_malloc(sizeof(char)*30);
	  pos = readString(pos, currnode->left->val.value.s, 30); 
	}
      }
    }
    //advance whitespace. Not needed here
    while (*pos==' '){
      pos++;
    }
    //check for operator
    if (isoperator(*pos)){
      //printf("operator %c read\n", *pos);
      //set the current node operator to the read operator
      currnode->operator = *pos;
      //advance position in string
      pos++;
    }
    //skip whitespace
    while (*pos==' '){
      pos++;
    }
    //read right hand side
    if (*pos == '('){
      //printf("( encountered, recursing on right tree\n");
      currnode->right = genNewNode();
      //the left side is not set
      pos = buildTree(pos+1, currnode->right, 0);
    }
    else {
      if (isdigit(*pos)){

	while (isdigit(*pos)){
	  *buffpos++ = *pos++;
	}
	*buffpos='\0';
	//sscanf(buffer, "%i", &val);
	val = read_int(buffer);

	//printf("read right value, %d\n",val);
	currnode->right = genNewNode();
	currnode->right->val.value.i = val;
	currnode->right->val.type = integer;
	buffpos=buffer;
      }
      else if (isalpha(*pos)){
	  pos = readVarName(pos, buffer);
	  //printf ("read varname %s on right side\n", buffer);
	  currnode->right = genNewNode();
	  strcpy(currnode->right->varname, buffer);
      }
      else if (*pos == '\"'){
	  currnode->left = genNewNode();
	  currnode->left->val.type = str;
	  currnode->left->val.value.s = (char *) my_malloc(sizeof(char)*30);
	  pos = readString(pos, currnode->left->val.value.s, 30); 
      }
    }
    //ending a level of recursion on the right side. Return
    if (*pos==')'){
      //printf(") encountered. Returning from recursion");
      pos++;
      return pos;
    }
      if (isoperator(*pos)){
      //push left
      //printf("additional operator. pushing tree left and reparsing");
      tmptree = genNewNode();
      tmptree->left = currnode->left;
      tmptree->operator = currnode->operator;
      tmptree->val = currnode->val;
      tmptree->result = currnode->result;
      tmptree->right = currnode->right;
      currnode->left = tmptree;
      currnode->operator='\0';
      currnode->right = NULL;
      leftset = 1;
      pos--;
    }
    else
      return pos;
    
  }
  //return position
  return pos;
}
