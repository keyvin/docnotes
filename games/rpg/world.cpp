#include "world.h"


world::world(){
  //maybe load a default. We are going with position 8,8,for now.
    pos_x = 20;
    pos_y = 10;
    //screen_x = 8;
    //screen_y = 8;
    view_size_x=20;
    view_size_y=12;
    make_map();
    current_view = new char *[view_size_y+1];
    for (int a = 0; a < view_size_y;a++){
      current_view[a] = new char[view_size_x+1];
    }
    update_view();
}

world::~world() {
  if (current_view)
    for (int a =0; a < view_size_y; a++){
      delete [] current_view[a];
    }
  delete [] current_view;
  
}

void world::make_map(){
  for (int y = 0; y <Y_MAX; y++){
    for (int x = 0; x < X_MAX; x++){
      if (x == 0 || x == (X_MAX)){
        current_map[y][x].type = WATER;
      }
      else if ((y == 0) || (y == Y_MAX) || y == Y_MAX-1) {
        current_map[y][x].type = WATER;
      }
      else {
        current_map[y][x].type = LAND;
      }
    }
  }

  return;
}

char world::map_type_to_char(cell_type a){
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
  int x,y;
  for (y = 0; y< view_size_y; y++){
    printf("%s\n", current_view[y]);
  }
}

//Returns a character in the current view
char world::view_at(int x, int y) {
  if ( (x>=0) && (x < view_size_x) &&
        (y>=0) && (y < view_size_y)) {
    return current_view[y][x];
  }
  return '\0';
}

  

void world::update_view(){
    /*Centered on the position*/
    int port_x, port_y;
    int map_absolute_x, map_absolute_y;
    view_size_x, view_size_y, pos_x, pos_y;
    /*is view size_x and view size y odd?*/
    //assume yes
    //char outbuffer[X_MAX+1];
    port_x = (int) (view_size_x/2);
    port_y = (int) (view_size_y/2);
    int curr_x, curr_y;
    curr_x = curr_y =0;
    for (curr_y = -port_y; curr_y != port_y; curr_y++) {
      map_absolute_y = pos_y + curr_y + port_y;

      if (pos_y + curr_y < 0 || pos_y + curr_y > Y_MAX-1 ){
 	  
	    for (int a = 0; a !=view_size_x; a++){
               current_view[curr_y+port_y][a] = 'W';
        }
        //current_view[curr_y+port_y][view_size_x] = '\0';
        continue;
      }
       for (curr_x = -port_x; curr_x != port_x; curr_x++ ) {
        map_absolute_x = pos_x + curr_x + port_x;
            if (pos_x+curr_x <0 || pos_x + curr_x >= X_MAX) {
                 current_view[curr_y+port_y][curr_x+port_x] = 'W';

             }
            else {
                current_view[curr_y+port_y][curr_x+port_x] = map_type_to_char(
                       current_map[pos_y+curr_y][pos_x+curr_x].type);
            }

        }
        //current_view[curr_y+port_y][view_size_x]='\0';
    }
}

bool world::is_passable(int x, int y) {
  if (x < 0 || x >= X_MAX || y < 0 || y >= Y_MAX)
    return (false);
  if (current_map[y][x].type != LAND){
    return (false);
  }
  return(true);
}

bool world::north() {
  if (!is_passable(pos_x, pos_y-1))
    return false;
  --pos_y;
  return true;
}

bool world::south() {
  if (!is_passable(pos_x, pos_y+1))
    return false;
  ++pos_y;
  return true;

}

bool world::east() {
  if (!is_passable(pos_x+1, pos_y))
    return false;
  ++pos_x;
  return true;


}

bool world::west() {
  if (!is_passable(pos_x-1, pos_y))
    return false;
  --pos_x;
  return true;
}


