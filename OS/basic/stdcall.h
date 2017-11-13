#ifndef STDCALL
#define STDCALL 1
#define freestanding 1
#ifdef  freestanding 
#define isdigit my_isdigit 
#define isalpha my_isalpha
#define NULL 0
int my_isdigit(char);
int strcmp(char *, char *);
int strncmp(char *, char *, int);
int strcpy(char *, char *);
int memset(char *, char, int);
int strlen(char *);
int strcat(char*, char*);
void * my_free(void *);
void *my_malloc(int);

void *memory_block;
int read_int(char *);
int inttoa(int, char *);
int my_isalpha(char);
#else
//#include <string.h>
#endif


#endif
