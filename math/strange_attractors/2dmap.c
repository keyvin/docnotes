#include "include/valuetable.h"
#include <math.h>
#include <stdlib.h>
#include <stdio.h>

int test_attractor()
{
  int max_iter = 11000;
  int xmin = -1000000;
  int xmax = -1* xmin;
  int  p = 0;
  float lsump = 0;
  float n =0;
  float nl = 1;
  float xn = 1;
  float xn_1 = 0;
  int ymax = 0;
  int ymin = 0;
  float lsum = 0;
  float lup = 0;
  init_table();
  generate_string(5);

  while (n < max_iter)
  {
    n++;
    xn_1 = coefficient[attractor_name[0]-' '] + (coefficient[attractor_name[1]-' '] +(coefficient[attractor_name[2]-' ']*xn)*xn);
    //if (n < 100) || (n > 1000)
    //calculate L exponent
    float df = coefficient[attractor_name[1]-' '] + 2.0*coefficient[attractor_name[2]-' ']*xn;
    if (df < 0.0 ) df = df * -1.0;
    if (df > 0.0) nl+=1.0;	     
    lsum = lsum+log(df);
    lup = .721347*lsum/nl;
    printf("attractor - %s: xn - %f, xn_1 - %f, lup-%f, df - %f, lsum - %f\n", attractor_name, xn, xn_1, lup, df, lsum);
    if (n == max_iter)
    {
      printf("Is attractor - %s", attractor_name);
	getc(stdin);
      return 0;
    }
    if (xn_1 > 1000000.0 || xn_1 <-1000000.0)
    {
      //break
      break;
    }
    if (xn_1 - xn < .00001 && xn_1 - xn > -.00001)
    {
     	
	 break;
    }
    if ((n > 100) && (lup < .005))
    {
	break;
    }
	xn = xn_1;
		     
}    
  	
    //if (xn < xmin) xmin = xn;
      //if (xn > xmax) xmax = xn;
      //ymin = xmin;
      //ymax = xmax
	getc(stdin);
return n;
}





int main()
{
  
while (1)
    {
//	int res = test_attractor();
	test_attractor() ;
//	getc(stdin);
	}
      
  
  return 0;
}
