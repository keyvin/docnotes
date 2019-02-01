#ifndef CONTROLLER_H
#define CONTROLLER_H
#include <iostream>
#include <string>
#include <vector>
#include "screen.h"
#include "world.h"
class controller {

 private:
  int internal;
  world *current_world;
  screen *current_screen;
  
 public:
  controller(world *, screen *);
  void process_input(char );
    
};

#endif
