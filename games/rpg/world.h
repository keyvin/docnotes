#ifndef WORLD_H
#define WORLD_H
#include <cstdio>

#define X_MAX 200
#define Y_MAX 200

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
    char **current_view; 
public:
    int view_size_x, view_size_y;
    world();
    ~world();
    char map_type_to_char(cell_type);
    void make_map();
    void dump_map();
    void show_view();
    void update_view();
    char view_at(int, int);
    bool south();
    bool north();
    bool east();
    bool west();
    bool is_passable(int, int);
};

#endif // WORLD_H
