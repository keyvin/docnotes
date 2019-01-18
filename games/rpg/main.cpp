#include <iostream>
#include "world.h"
#include <ncurses.h>

using namespace std;

int main()
{
  WINDOW *mainw;
    world a;
    cout << "Hello World!" << endl;
    mainw = initscr();
    a.dump_map();
    a.show_view();
    getch();
    refresh();


    endwin();
    return 0;
}
