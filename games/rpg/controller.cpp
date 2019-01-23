#include "controller.h"

controller::controller(world *crr, screen *cvv){
  current_world = crr;
  current_screen = cvv;
}



//I could do something here with a map and function pointers, but not now.

void controller::process_input(char in){
  switch (in) {
  case 'h':
    current_world->west();
    break;
  case 'j':
    current_world->south();
    break;
  case 'k':
    current_world->north();
    break;
  case 'l':
    current_world->east();
    break;
  }
}
