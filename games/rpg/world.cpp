#include "world.h"


world::world(){
//maybe load a default. We are going with position 8,8,for now.
    pos_x = 8;
    pos_y = 8;
    make_map();
}

void world::make_map(){
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

char world::map_type_to_char(enum cell_type a){
  //Internals of this function can change as necessary
  switch (a) {
      case MOUNTAIN:
    return 'M';

      case WATER:
    return 'W';

      case LAND:
    return 'L';

  }

 return 'D';
}

void world::dump_map() {
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

void world::show_view(){
    /*Centered on the position*/
    int port_x, port_y;
    view_size_x, view_size_y, pos_x, pos_y;
    /*is view size_x and view size y odd?*/
    //assume yes
    char outbuffer[view_size_x+1];
    port_x = (int) (view_size_y/2);
    port_y = (int) (view_size_x/2);
    int curr_x, curr_y;
    curr_x = curr_y =0;
    for (curr_x = -port_x; curr_x != port_x; curr_x++)
        for (curr_y = -port_y; curr_y != port_y; curr_y++ ) {
            if (pos_y+curr_y < 0 || pos_y+curr_y > Y_MAX)
            else if (pos_x+curr_x <0 || pos_x + curr_x > X_MAX) {
                outbuffer[curr_x] = 'W';

            }
            else
            {
                outbuffer = map_type_to_char[]
            }

        }
}

