//#include <stdlib.h>
#define freestanding 1
//This file has all stdlib, stdio, string, and conversion macros

#ifdef freestanding
#include "stdcall.h"
int my_isalpha(char c){
  if (c >= 'a' && c <= 'z')
    return 1;
  if (c >= 'A' && c <= 'Z')
    return 1;
  return 0;
}

int my_isdigit(char c){
  if (c >= '0' && c<= '9'){
    return 1;
  }
  return 0;
}

//int strlen(char *target){
// int length = 0;
//  while (*target != '\0'){
//    length++;
//    target++;

//  }
//  return length;
//}

int strcmp(char *s1, char *s2){
  int difference = 0;
  difference = *s1 - *s2;
  while ((*s1 != '\0') && (*s2 != '\0')){
    if (*s1 == *s2)
     {
      s1++;
      s2++;
     }
    else
      return 1;
  }
    
  return 0;
}

int strncmp(char *s1, char *s2, int num)
{
  int difference = 0;
  int cnt = 0;
  difference = *s1 - *s2;
  while ((!difference) && (cnt < num))
  {
    s1++;
    s2++;
    cnt++;
    difference = *s1 - *s2;
    if (*s1 != '\0' || *s2 !='\0')
      break;
  }
  return difference;
}

int strcpy(char *target, char *source){
  while (*source != '\0'){
    *target = *source;
    target++;
    source++;
  }
  return 0;
}

int memset(char *buffer, char fill, int num){
  int a = 0;
  for (a=0; a < num; a++)
    {
      buffer[a] = fill;
    }
  return 0;

}

int strcat(char *target, char *src){
  int len = 0;
  len = strlen(target);
  while(*src != '\0'){
    target[len] = *src;
      src++;
      target++;

  }
  target[len+1] = '\0';
}

//just wrap calls
#endif


#ifdef freestanding
void *memory_block;
//#include <stdlib.h>
void * my_malloc(int bytes){
  // memory pool hasn't been initialized
  //This will just be an address later. 
  void *start;
  if (!memory_block)
    memory_block = (void *)0xFFFF20;
  start = memory_block;
  memory_block = memory_block+bytes+10; 
  return start;
}

void *my_free(void *s){
  return NULL;
}

int read_int(char *source){
  int retval = 0;
  while (isdigit(*source)){
    retval = retval + *source - 48;
    source++;
    if (isdigit(*source)){
      retval = retval* 10;
    }
  }
  return retval;
}

//buffer provided by parent.
int inttoa(int con, char *buffer){
    int working = con;
    int tmp = 0;
    int pos = 0;
    char tmp_buffer[25];
    while (working != 0){
      tmp = working %10;
      tmp_buffer[pos] = tmp + 48;
      pos++;
      working = working /10; //should truncate, not round
    }
    tmp_buffer[pos] = '\0';
    tmp = 0;

    //reverse
    for (int a = pos-1; a >= 0; a--){
      buffer[tmp] = tmp_buffer[a];
      tmp++;
    }
    buffer[pos] = '\0';
    return 0;  
}


#endif  
  


  

