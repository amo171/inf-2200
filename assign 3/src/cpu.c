/** @file cpu.c
 *  @brief This code simulates a system with caching between the CPU and the
 *  main memory.
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "memory.h"
#include "byutr.h"



/*
 * Command line argument: Trace file.
 */
int cachesim(int argc, char *argv[], int *input)
{
	clock_t start = clock(), diff;
	FILE *tracef;
	p2AddrTr tr;

	if (argc < 2)
	{
		printf("Usage: %s filename\n", argv[0]);
		exit(1);
	}

	/* fopen(argv[1], "r") -> fopen(argv[1], "rb")
	 * Windows doesn't follow POSIX here and fopen needs the 'b' to function
	 * properly.
	 */
	if ((tracef = fopen(argv[1], "rb")) == NULL)
	{
		printf("Could not open file: %s\n", argv[1]);
		exit(1);
	}

	/* Initialize the memory subsystem */
	memory_init(input[0], input[1], input[2], input[3], input[4], input[5], input[6], input[7]); 


	/* Loop through the trace file and simulate memory accesses */
	while (!feof(tracef))
	{
		if (fread(&tr, sizeof(p2AddrTr), 1, tracef) == 1)
		{
			switch(tr.reqtype)
			{
			case FETCH:    memory_fetch(tr.addr, NULL); break;
			case MEMREAD:  memory_read(tr.addr, NULL); break;
			case MEMWRITE: memory_write(tr.addr, NULL); break;
			default: printf("Ignoring trace record with type %d\n", tr.reqtype);
			}
		}
	}

	fclose(tracef);

	memory_finish(); /* Deinitialize the memory subsystem */

	diff = clock() - start;

	int msec = (float)diff * 1000 / CLOCKS_PER_SEC;
	printf("Time taken %d seconds %d milliseconds\n", msec/1000, msec%1000);

	return 0;
}

void printsettings(int *input){
	if (input[8] == 0){
		printf("\t*************************************************\n"
			   "\t*		32 KB cache  			*\n"
			   "\t*************************************************\n");
	}
	if (input[8] == 1){
		printf("\t*************************************************\n"
			   "\t*		16 KB cache 	  		*\n"
			   "\t*************************************************\n");
	}
	if (input[8] == 2){
		printf("\t*************************************************\n"
			   "\t*		8 KB cache  	  		*\n"
			   "\t*************************************************\n");
	}
	if (input[8] == 3){
		printf("\t*************************************************\n"
			   "\t*		4 KB cache  	  		*\n"
			   "\t*************************************************\n");
	}
	if (input[8] == 4){
		printf("\t*************************************************\n"
			   "\t*		2 KB cache 	  			*\n"
			   "\t*************************************************\n");
	}
	if (input[8] == 5){
		printf("\t*************************************************\n"
			   "\t*		1 KB cache	  			*\n"
			   "\t*************************************************\n");
	}
	
	printf( "\t------cache settings------\n"
					"\tL1 cache: \t\t\t\t%d KB\n"
					"\tL1 Block size:\t\t\t\t%d Bytes\n"
					"\tassociativity L1-instruction cache: \t%d-way \t\n"
					"\tassociativity L1-data cache: \t\t%d-way \t\t\n"
					"\tL2 cache: \t\t\t\t%d KB\n"
					"\tassociativity L2-unified cache: \t%d-way \t\n"
					"\tBlock size L2 \t\t\t\t%d ytes \n", 
					input[0], 
					input[1], 
					input[2], 
					input[3], 
					input[4], 
					input[5], 
					input[6]);
	if (input[7])
		printf("\t\tWrite Back is active\n");
	else
		printf("\t\tWrite Through is active\n");
	printf("\t-----------------------------\n");
}

int main(int argc, char *argv[]){
	int input[9];


/*-------standard configuration------*/
	input[0] = 32;  //KB size of the L1 cache
	input[1] = 64;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 4;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 64;  //byte size of the blocks in L2 Cache
	input[7] = 0;   //writeback policy
	input[8] = 0;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);


/*------16 -Way associativity -------*/
/*	input[0] = 32;  //KB size of the L1 cache
	input[1] = 512;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 16;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 512;  //byte size of the blocks in L2 Cache
	input[7] = 1;   //writeback policy
	input[8] = 1;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);*/

/*-------8 -Way associativity---------*/
/*	input[0] = 32;  //KB size of the L1 cache
	input[1] = 512;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 8;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 512;  //byte size of the blocks in L2 Cache
	input[7] = 1;   //writeback policy
	input[8] = 2;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);
*/
/*-------4 -Way associativity---------*/
/*	input[0] = 32;  //KB size of the L1 cache
	input[1] = 512;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 4;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 512;  //byte size of the blocks in L2 Cache
	input[7] = 1;   //writeback policy
	input[8] = 3;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);*/

/*--------2 -Way associativity-----------*/
/*	input[0] = 32;  //KB size of the L1 cache
	input[1] = 512;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 2;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 512;  //byte size of the blocks in L2 Cache
	input[7] = 1;   //writeback policy
	input[8] = 4;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);*/

/*--------1 -Way associativity---------*/
/*	input[0] = 32;  //KB size of the L1 cache
	input[1] = 512;  //byte size of the blocks in L1 Cache
	input[2] = 4;   //associativity of L1_Instruction Cache
	input[3] = 1;   //associativity of L1_Data Cache
	input[4] = 256; //KB size of the L2 cache
	input[5] = 8;   //associativity of L2_unified Cache
	input[6] = 512;  //byte size of the blocks in L2 Cache
	input[7] = 1;   //writeback policy
	input[8] = 5;   //just for printsettings
	// forced Least Recently Used Policy
	printsettings(input);
	cachesim(argc, argv, input);*/
}
