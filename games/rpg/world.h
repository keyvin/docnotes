#ifndef WORLD_H
#define WORLD_H
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#define X_MAX 100
#define Y_MAX 100

//typedef int map_cell;
typedef unsigned short BOOL;



enum cell_type { MOUNTAIN, LAND, FOREST, WATER, RIVER };

typedef struct MAP_CELL {
  enum cell_type type;
  BOOL passable;
} map_cell;

map_cell current_map[X_MAX][Y_MAX];

void make_map();
void dump_map();

#endif

  


