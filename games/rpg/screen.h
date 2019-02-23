#ifndef SCREEN_H 
#define SCREEN_H
//#include <ncurses.h>
#include "world.h"
class screen {

 private:
  //SCREEN *scrn;

 public:

  int map_char_to_color(char);
  ~screen();
  screen();
  void do_draw();
  void draw_bar();
  void draw_world(world *);
   
};
   
#endif
