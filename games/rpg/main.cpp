#include <iostream>
#include "world.h"


using namespace std;

int main()
{
    world a;
    cout << "Hello World!" << endl;
    a.dump_map();
    a.show_view();
    return 0;
}
