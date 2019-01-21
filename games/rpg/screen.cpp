#include "screen.h"
#include "world.h"

int screen::map_char_to_color(char c){
  switch (c) {
  case 'W':
    return 2;
  case 'L':
    return 1;
  }
  return 0;

}

screen::screen() {
  //init the ncurses reference
  initscr();
  printw("Screen initialized");
  refresh();
  start_color();
  init_pair(1, COLOR_GREEN, COLOR_BLACK);
  init_pair(2, COLOR_BLUE, COLOR_BLACK);
  noecho();
  raw();
  
}

screen::~screen() {
  endwin();
}

//replace world with a singleton eventually
void screen::draw_world(world *curr_world) {
  for (int y = 0; y != curr_world->view_size_y; y++) {
    for (int x = 0; x != curr_world->view_size_x; x++) {
      char curr = curr_world->view_at(x, y);
      int color = map_char_to_color(curr);
      if (color) {
	attron(COLOR_PAIR(color));
	mvaddch(y,x,curr);
	attroff(COLOR_PAIR(color));
      }
      
    }
  }
  refresh();
  
}
