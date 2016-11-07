#include <stdio.h>
#include <stdlib.h>

#define LIMIT 250000000 /*size of integers array*/

int main(){
    unsigned long long int i,j;
    int *primes;
    int z = 1;

    primes = malloc(sizeof(int)*LIMIT);

    for (i=2;i<LIMIT;i++)
        primes[i]=1;

    for (i=2;i<LIMIT;i++)
        if (primes[i])
            for (j=i;i*j<LIMIT;j++)
                primes[i*j]=0;

    //for (i=2;i<LIMIT;i++)
      //  if (primes[i])
        //    printf("%dth prime = %dn\n",z++,i);

return 0;
}


//source http://www.programminglogic.com/the-sieve-of-eratosthenes-implemented-in-c/