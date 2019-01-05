#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "world.h"
/*Functions for reading and writing world state*/

void make_map(){
  for (int x = 0; x <X_MAX; x++){
    for (int y = 0; y < Y_MAX; y++){
      if (x == 0){
	current_map[y][x].type = WATER;
      }
      else if (x == (X_MAX-1)){
	current_map[y][x].type = WATER;
      }
      else if (y == 0) {
	current_map[y][x].type = WATER;
      }
      else if (y == Y_MAX-1) {
	current_map[y][x].type = WATER;
      }
      else {
	current_map[y][x].type = LAND;
      }
    }
  }         
  return;
}

char map_type_to_char(enum cell_type a){
  //Internals of this function can change as necessary
  switch (a) {
      case MOUNTAIN:
	return 'M';

      case WATER:
	return 'W';

      case LAND:
	return 'L';

  }
    

}

void dump_map() {
  char outbuffer[X_MAX+1];
  for (int y = 0; y < Y_MAX; y++){
    for (int x = 0; x < X_MAX; x++){
      outbuffer[x] = map_type_to_char(current_map[y][x].type);
    }
    outbuffer[X_MAX] = '\0';
    printf("%s\n", outbuffer);
  }
  return;
}

