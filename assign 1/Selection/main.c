#include <stdio.h>
#include <stdlib.h>


extern void selection_sort (int *arr, int size);


void
_selection_sort (int *arr, int size)
{
  int i, j, min, tmp;
  
  for (i = 0; i < size; i++)
  {
    min = i;
    for (j = i + 1; j < size; j++)
    {
      if (arr[j] < arr[min])
        min = j;
    }
    
    if (min != i)
    {
      tmp = arr[i];
      arr[i] = arr[min];
      arr[min] = tmp;
    }
  }
}



int
main (void)
{
  int i, num_elems;
  static int my_arr[] = { -13, 5, 7, 1, 17, 56, 22, 21, 8, 5, 2, 4, 3, 11, 17, 10, 18, 16, 102, 6 };
  num_elems = sizeof (my_arr) / sizeof (int);
  
  selection_sort (my_arr, num_elems);
  
  for (i = 0; i < num_elems; i++)
  {
    fprintf (stdout, "%d\n", my_arr[i]);
  }
  
  return 0;
}
