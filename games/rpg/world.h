#ifndef WORLD_H
#define WORLD_H




#define X_MAX 100
#define Y_MAX 100

enum cell_type { MOUNTAIN, LAND, FOREST, WATER, RIVER };

typedef struct MAP_CELL {
  enum cell_type type;
  BOOL passable;
} map_cell;

class world
{
private:
    map_cell current_map[X_MAX][Y_MAX];

public:
    world();
    void make_map();
    void dump_map();
};

#endif // WORLD_H
