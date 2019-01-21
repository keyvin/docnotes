#include <iostream>
#include "world.h"
#include <ncurses.h>
#include "screen.h"
#include "controller.h"

using namespace std;

int main()
{
  
    world a;
    screen c; //begins a screen window
              //Turns off cbreak
    controller d(&a, &c);
    c.draw_world(&a);
    char in;
    while ((in = getch()) != 'Q'){
      d.process_input(in);
      a.update_view();
      c.draw_world(&a);
      refresh();
    }
    return 0;
}
