#include <stdio.h>
#include "valuetable.h"


int main(int argv, char **argc)
{
  init_table();
  for (int a = 0; a< TABLE_LENGTH; a++){
    printf("%c - %f\n", ascii[a], coefficient[a]);
  }

  generate_string(12);
  printf("attractor: %s", attractor_name);
  return 0;
}
