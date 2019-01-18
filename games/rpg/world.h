#ifndef WORLD_H
#define WORLD_H
#include <cstdio>

#define X_MAX 100
#define Y_MAX 100

typedef enum CELL_TYPE { MOUNTAIN, LAND, FOREST, WATER, RIVER } cell_type;

typedef struct MAP_CELL {
  cell_type type;
  bool passable;
} map_cell;

class world
{
private:
    map_cell current_map[X_MAX][Y_MAX];
    int pos_x, pos_y;
    int view_size_x, view_size_y;
    map_cell ** current_view; 
public:
    world();
    ~world();
    char map_type_to_char(cell_type);
    void make_map();
    void dump_map();
    void show_view();
    void update_view();
};

#endif // WORLD_H
