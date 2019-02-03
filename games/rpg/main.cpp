#include <iostream>
#include "world.h"
#include <ncurses.h>
#include "screen.h"
#include "controller.h"
#include "time.h"

using namespace std;

int main()
{
  unsigned int count = 0;
  clock_t then, now;
  struct timespec sleep_timer = { 0, 0};
  struct timespec remainder;
  unsigned long target_t = CLOCKS_PER_SEC / 60;
  world a;
    screen c; //begins a screen window
              //Turns off cbreak
    controller d(&a, &c);
    c.draw_world(&a);
    raw();
    char in;
    timeout(0);
    while ((in = getch()) != 'Q'){
      printw("%c", in);
      then = clock();
      d.process_input(in);
      a.update_view();
      c.draw_world(&a);
      
      now = clock();
      
      
      if (then > now) {
	//this case is reached if we have wrapped the cpu time
	;
      }
      if ((now - then) < target_t){
	sleep_timer.tv_nsec = now - then;
	nanosleep(&sleep_timer, &remainder);
      }
      count++;
      if (count % target_t == 0){
	mvprintw(10, 50, "%u   ", count/target_t);
      }
    }
    return 0;
}
