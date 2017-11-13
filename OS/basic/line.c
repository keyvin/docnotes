#include "line.h"
//#include <stdlib.h>
//#include <string.h>
//#include <stdio.h>
#include "stdcall.h"
#include "parse.h"
#include "parsetree.h"
#include "varlist.h"

void terminal_writestring(const char *data);

line * newLine(char *addline){
  char buffer[200];
  char *pos= addline;
  char *target = buffer;
  line *newline = (line *) my_malloc(sizeof(line));
  
  if (!isdigit(*pos)){
    //printf("Invalid line - must start with line number: %s", addline);
    return NULL;
  }
  while (isdigit(*pos)){
    *(target++)= *(pos++);
  }
  *target = '\0';
  //sscanf(buffer,"%d", &(newline->lineno));
  newline->lineno = read_int(buffer);
  pos++;
  strcpy(newline->instruction, pos);
  newline->next = NULL;
  newline->prev = NULL;
  return newline;
}

line * insertLine(line *list, line *toinsert){
  line *position = list;
  if (!list)
    return toinsert;
  /*equal to head of list*/
  if (toinsert->lineno == list->lineno){
    toinsert->next = list->next;
    my_free(list);
    return toinsert;
  }
  /*less than head of list, make new head*/

  if (toinsert->lineno < list->lineno){
    list->prev = toinsert;
    toinsert->next = list;
    return toinsert;
  }

  while (position->next){
    /*equal to position but not at head of list, replace*/
     if (position->lineno == toinsert->lineno){
      position->prev->next = toinsert;
      toinsert->next = position->next;
      my_free(position);
      return list;
     }
     /*insert sorted*/
     if (position->lineno > toinsert->lineno){
       toinsert->prev = position->prev;
       toinsert->next = position;
       position->prev->next = toinsert;
       position->prev = toinsert;
       return list;
     }
     position = position->next;
  }
  /*replace end of list*/
  if (position->lineno == toinsert->lineno){
      position->prev->next = toinsert;
      toinsert->next = position->next;
      my_free(position);
      return list;
  }
  /*append to end of list*/
  if (position->lineno > toinsert->lineno){
    toinsert->prev = position->prev;
    toinsert->next = position;
    position->prev->next = toinsert;
    position->prev = toinsert;
    return list;
  }
  position->next = toinsert;
  toinsert->prev = position;
  return list;
  
}

void printList(line *head)
{
  char buffer[120];
  while (head){
    inttoa(head->lineno, buffer);
    terminal_writestring(buffer);
    terminal_writestring(" ");
    terminal_writestring(head->instruction);
    terminal_writestring("\n");
    //printf("%d %s\n", head->lineno, head->instruction);
    //x
    head = head->next;
  }
  return;
}


line *executeLine(line *toexec, var *varlist){
  char tmpbuffer[100];
  char *despaced = NULL;
  evaltree *root = NULL;
  char * startpos = NULL;
  int counter = 0;
  root = genNewNode();
  if (!toexec){
    return NULL;
  }
  despaced = deSpace(toexec->instruction);
  startpos = toexec->instruction;
  
  if (strncmp(toexec->instruction, "SET", 3)==0){
      startpos = readVarName(startpos+4, tmpbuffer);
      //skip equals when parsing
      startpos++;
      //tmpbuffer[strlen(tmpbuffer)-1]= '\0';
      buildTree(startpos, root, 0);
      calcTree(root, varlist);
      setVar(varlist, tmpbuffer, root->result);    
  }
  if (strncmp(toexec->instruction, "PRINT", 5)==0){
    startpos+=6;
    buildTree(startpos, root, 0);
    calcTree(root, varlist);
    if (root->result.type == integer){
      inttoa(root->result.value.i, tmpbuffer);
      
      terminal_writestring(tmpbuffer);
      terminal_writestring("\n");
      //printf("%s\n", tmpbuffer);
      //printf("%d\n", root->result.value.i);
    }
    if (root->result.type == str) {
      //printf("%s\n", root->result.value.s);
	terminal_writestring(root->result.value.s);
	
    }
  }
  if (strncmp(toexec->instruction, "GOTO", 5)==0){
    startpos+=5;
    buildTree(startpos, root, 0);
    calcTree(root, varlist);
    if (root->result.value.i ==  toexec->lineno){
      //printf ("Pointless infinite loop at line %d\n", toexec->lineno);
      return NULL;
    }
    if (root->result.value.i < toexec->lineno){
      while (toexec->prev){
	toexec = toexec->prev;
	if (toexec->lineno == root->result.value.i)
	  return toexec;
      }
      return NULL;
    }
    if (root->result.value.i > toexec->lineno){
      while (toexec->next){
	toexec = toexec->next;
	if (toexec->lineno == root->result.value.i)
	  return toexec;
      }
      return NULL;
    }
    return NULL;
  }
  if (strncmp(toexec->instruction, "IF", 2)==0){
    startpos+=3;
    buildTree(startpos, root, 0);
    calcTree(root, varlist);
    if (root->result.value.i != 0){
      return toexec->next;
    }
    while(toexec->next){
      toexec=toexec->next;
      //keep track of nested if then else
      if (strncmp(toexec->instruction, "IF",2)==0)
	counter++;
      if ((strncmp(toexec->instruction, "ELSE", 4)==0)&&counter==0)
	return toexec->next;
      if (strncmp(toexec->instruction, "END IF", 6)==0)
	counter--;
    }
    return NULL;
  }
  if (strncmp(toexec->instruction, "ELSE", 4)==0){
    while (toexec->next){
      toexec=toexec->next;
      if (strncmp(toexec->instruction, "IF",2)==0)
	counter++;
      if ((strncmp(toexec->instruction,"END IF", 6)==0)&&counter==0)
	return toexec->next;
      if (strncmp(toexec->instruction, "END IF", 6)==0)
	counter--;
    }
    return NULL;
  }
  if (strncmp(toexec->instruction, "WHILE", 5)==0){
    //    printf("In While at line %d", toexec->lineno);
    startpos+=6;
    buildTree(startpos, root,0);
    calcTree(root,varlist);
    if (root->result.value.i !=0)
      return toexec->next;
    while(toexec->next){
      toexec = toexec->next;
      if (strncmp(toexec->instruction, "WHILE", 5)==0)
	counter++;
      if (strncmp(toexec->instruction, "WEND", 4)==0&&counter==0)
	return toexec->next;
      if (strncmp(toexec->instruction, "WEND", 4)==0)
	counter--;
    }
    return NULL;
  }

  if (strncmp(toexec->instruction, "WEND", 4)==0){
    while (toexec->prev){
      toexec=toexec->prev;
      if (strncmp(toexec->instruction, "WEND", 4)==0)
	counter++;
      if (strncmp(toexec->instruction, "WHILE", 5)==0&&counter==0)
	return toexec;
      if (strncmp(toexec->instruction, "WHILE", 5)==0)
	counter--;
    }
    return NULL;
  }
  my_free(despaced);
  freeTree(root);
  return toexec->next;
}
