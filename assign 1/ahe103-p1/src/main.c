#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

// Declaring that assembly function is provided elsewhere
extern void asm_function();

// This should be the C equivalent to the assembly implementation
void c_function(int *primes,int LIMIT) {
	int i, j;

    for (i=2;i<LIMIT;i++)
        if (primes[i])
            for (j=i+i; j<LIMIT; j+=i)
                primes[j]=0;

    //for (i=2;i<LIMIT;i++)
        //if (primes[i])
            //printf("%dth prime = %dn\n",z++,i);
}
//
//
//source http://www.programminglogic.com/the-sieve-of-eratosthenes-implemented-in-c/
//
//

void fillarray(int *primes, int LIMIT){
	int i;
	for (i=0;i<LIMIT;i++)
		primes[i]=1;
}
void test_print(int *primes, int LIMIT) {
	int i;
	for (i=0;i<LIMIT;i++){
    	if (primes[i])
        	printf("%d - ", i);
	}
}

void compare_function(int *asmprimes, int *cprimes, int LIMIT){
	int i;
	int fail = 0;
	for (i=0; i<LIMIT; i++){
		if (asmprimes[i] == cprimes[i]){
		}
		else
			fail = 1;
		if (fail){
			printf ("fail\n");
			break;
		}
	}
	if (!fail) {
		printf ("Arrays are equal\n");
	}
}
void main(int argc, char **argv) {

	int LIMIT = atoi(argv[1]); /*size of integers array*/
	int *asmprimes;
	int *cprimes;
	time_t before_c, after_c;
	time_t before_asm, after_asm;
	cprimes = malloc(sizeof(int)*LIMIT);
	asmprimes = malloc(sizeof(int)*LIMIT);

	printf("fillarray\n");
	fillarray(asmprimes, LIMIT);
	fillarray(cprimes, LIMIT);
	printf("endfill\n");
	//before_c = clock();
	c_function(cprimes, LIMIT);
	//after_c = clock();
	//printf ("c_function uses %f seconds\n",((double)after_c - (double)before_c)/1000000);
	//before_asm = clock();
	//asm_function(asmprimes, LIMIT);
	//after_asm = clock();
	//printf ("asm_function uses %f seconds\n",((double)after_asm - (double)before_asm)/1000000);
	//compare_function(asmprimes, cprimes, LIMIT);
	//test_print(cprimes, LIMIT);
	//test_print(asmprimes, LIMIT);


}
