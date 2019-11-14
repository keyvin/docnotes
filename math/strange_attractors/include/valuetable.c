#include <stdlib.h>
#include <time.h>
#include "valuetable.h"


void generate_string(int length)
{
  //assumptin is buffer will always 
  length = (length<MAX_NAME_LENGTH) ? length: MAX_NAME_LENGTH;
  for (int a = 0; a < length; a++)
  {
    attractor_name[a] = ascii[rand() %TABLE_LENGTH];
  }
  attractor_name[length] = '\0';
  return;
}

void init_table()
{
  srand(time(0));
  for (int a = 0; a < TABLE_LENGTH; a++)
  {
    ascii[a] = ' ' + a;
    coefficient[a] = ((float)a)/10.0 + -4.5;
  }
  return;
}


