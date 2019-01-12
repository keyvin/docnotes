#ifndef VIEW_H
#define VIEW_H

#include <stdio.h>
#include <stdlib.h>
#include "world.h"

/*This header file defines functions that 
  create a view (what is currently visible)
  This is a composite of all possible objects
  FOV, fog of war, etc, etc */


unsigned int view_size_y = 0;
unsigned int view_size_x = 0;


/*initialization functions*/

int init_view(int, int);
int resize_view(int, int);
int get_view_centered(int, int);
 



#endif
