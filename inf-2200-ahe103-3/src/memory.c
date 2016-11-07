/** @file memory.c
 *  @brief Implements starting point for a memory hierarchy with caching and RAM.
 *  @see memory.h
 */

#include "memory.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int l1misspenalty = 10;
static int l2misspentaly = 30;

//used for accurate calculation of hit ratio and AMAT
static int fetchcount = 0;
static int readcount = 0;
static int writecount = 0;

static unsigned long instr_count;

//writeback policy: 0 = write through, 1 = write back
static int writeback;


typedef struct block block_t;
struct block {
	data_t *data;
	unsigned int tag;
	int valid;
	int dirty;
	int age;
};

typedef struct set set_t;
struct set {
	block_t *block;
};

typedef struct cache cache_t;
struct cache {
	set_t *set;
	int blocksize;
	int cachesize;
	int numsets;
	int writeback;
	int associativity;
	int hit;
	int miss;

};



cache_t *l1_instr;
cache_t *l1_data;
cache_t *l2_unif;


cache_t *cache_init(int cachesize, int associativity, int blocksize){

	//make space for the cache itself
	cache_t *cache = (cache_t *)malloc(sizeof(cache_t));
	if (cache == NULL){
		printf("error creating cache");
		exit(1);
	}

	int numsets = (cachesize *1024)/(blocksize*associativity);
	cache->cachesize = cachesize;
	cache->numsets = numsets;
	cache->blocksize = blocksize;
	cache->associativity = associativity;
	cache->hit = 0;
	cache->miss = 0;

	//numset is the number of sets in the cache
	//set variables in the cache
	cache->set = (set_t *)malloc(sizeof(set_t) * numsets);

	if (cache->set == NULL){
		printf("error creating set");
		exit(1);
	}

	int i, j;

	//for each set make an array of blocks
	for (i=0; i < numsets; i++){
		block_t *temp = (block_t *)malloc(sizeof(block_t)*associativity);
		cache->set[i].block = temp;
		if (cache->set[i].block == NULL){
			printf("error in block");
			exit(1);
		}
	}

	//for each set and each block add values to the variables
	for (i = 0; i <numsets; i++){
		for (j = 0; j < associativity; j++){
		cache->set[i].block[j].data = 0;
		cache->set[i].block[j].tag = 0;
		cache->set[i].block[j].valid = 0;
		cache->set[i].block[j].dirty = 0;
		cache->set[i].block[j].age = 0;
		}
	}

	return cache;
}

void memory_init(int cachesize_l1, int blocksize_l1, int ass_l1_instr, int ass_l1_data,
				 int cachesize_l2, int ass_l2, int blocksize_l2, int wbtag)
{

	//write the wbtag from cpu.c to the static writeback flag
	writeback = wbtag;
	/* Initialize memory subsystem here. */
	l1_instr = cache_init(cachesize_l1, ass_l1_instr, blocksize_l1);
	l1_data = cache_init(cachesize_l1, ass_l1_data, blocksize_l1);
	l2_unif = cache_init(cachesize_l2, ass_l2, blocksize_l2);
	
	instr_count = 0;
}

unsigned int get_range(cache_t *cache, unsigned int address, char *type){

	//find the amount of bits needed by the cachesize
	int n = (int)log2((double)(cache->numsets));
	//find the amount of bits needed by the blocksize
	int m = (int)log2((double)(cache->blocksize/4));
	//the tag is the rest of n, m, and two thrash bits
	int tagsize = 32 - (m+n+2);

	//check for keywords in order to know how much to shift for the given keyword
	if (strcmp(type, "tag") == 0) {
		return address >> (n+m+2);
	}

	else if (strcmp(type, "index") == 0){
		//the index needs to overflow the tag to make it disappear leaving just the index when shifting down
		unsigned int index = address << tagsize;
		index = index >>(tagsize+2+m);
		return index;
	}

	return 0;

}

void age_inc(cache_t *cache){

	int i, j;
	//for every set, and every block the age needs to be incremented
	for (i=0; i < cache->numsets; i++){
		for (j=0; j < cache->associativity; j++){
			cache->set[i].block[j].age++;
		}
	}
}

unsigned int find_oldest(cache_t *cache, int index){
	int j;
	int oldest = 0;
	int toast = 0;

	//traverse the blocks at an indexed set to find which one has the highest age
	//that block is not needed and then is toast(killed)
	for (j=0; j<cache->associativity; j++){
		if (cache->set[index].block[j].age > oldest){
			oldest = cache->set[index].block[j].age;
			toast = j;
		}
	}
	return toast;
}

int check_cache(cache_t *cache, unsigned int address){

	//get the index and tag from the address based on the given cache
	unsigned int index 	= get_range(cache, address, "index");
	unsigned int tag 	= get_range(cache, address, "tag");

	//increment the caches block's age
	age_inc(cache);
	int i;

	//check if the blocks' tag in an indexed set is the same and is valid
	for (i=0; i < cache->associativity; i++){
		if (cache->set[index].block[i].tag == tag && cache->set[index].block[i].valid == 1){
			//record a hit and make the age of the block 0 as it was accessed recently
			cache->hit++;
			cache->set[index].block[i].age = 0;
			return 1;
		}
	}
	//otherwise a miss
	cache->miss++;
	return 0;
}

int check_dirtyblock(cache_t *cache, int setindex){

	//returns the dirty bit of the oldest block to see if other precautions needs to be taken
	int blockindex = find_oldest(cache, setindex);
	return cache->set[setindex].block[blockindex].dirty;
}

void insert_block(cache_t *cache, int set_index, unsigned int block_tag, int dirty){
	
	//find the oldest block's index
	int location = find_oldest(cache, set_index);
	//use that index to replace that block with the new one
	cache->set[set_index].block[location].tag = block_tag;
	cache->set[set_index].block[location].dirty = dirty;
	cache->set[set_index].block[location].age = 0;
	cache->set[set_index].block[location].valid = 1;

}


void cache_read_WT(cache_t *cache, unsigned int address, data_t *data)
{
	
	instr_count++;
	//check the given l1 cache for the given block
	int i = check_cache(cache, address);
	//if miss in l1
	if (i == 0){
		//set som indexes and tags
		int l1_set_index = get_range(cache, address, "index");
		int l2_set_index = get_range(l2_unif, address, "index");
		unsigned int l1_block_tag = get_range(cache, address, "tag");
		unsigned int l2_block_tag = get_range(l2_unif, address, "tag");

		//check for the tag in 
		int j = check_cache(l2_unif, address);
		//if miss in l2

		if (j == 0){
			//write the set index and tag of the data to l2 from "ram" spoofed by l2
			insert_block(l2_unif, l2_set_index, l2_block_tag, 0);
			insert_block(cache, l1_set_index, l1_block_tag, 0);
			//return the newly fetched data from ram
			return;
		} 
		// else hit in l2
		else {
			
			//write the set index and the block tag to l1 
			insert_block(cache, l1_set_index, l1_block_tag, 0);
			//return the data fetched from L2
			return;
		}
	}
	// hit in l1
	else {
		//return the data
		return;
	}
}

void cache_read_WB(cache_t *cache, unsigned int address, data_t *data)
{
	
	instr_count++;
	int i = check_cache(cache, address);
	//if miss in l1
	if (i == 0){
		//find the set and index for the address based on L1 cache
		int l1_set_index = get_range(cache, address, "index");
		unsigned int l1_block_tag = get_range(cache, address, "tag");

		//check if the block is dirty
		if (check_dirtyblock(cache, l1_set_index)){

			//find the set and index for the addres based on L2 cache to put the dirty bit into it
			int l2_set_index = get_range(l2_unif, address, "index");
			unsigned int l2_block_tag = get_range(l2_unif, address, "tag");
			insert_block(l2_unif, l2_set_index, l2_block_tag, 0);
		
		}

		int j = check_cache(l2_unif, address);
		//if miss in l2

		if (j == 0){
			//write 
			insert_block(cache, l1_set_index, l1_block_tag, 1);
			//return the data fetched from RAM
			return;
		} 
		else {
			// else hit in l2
			//write the set index and the block tag to l1 
			insert_block(cache, l1_set_index, l1_block_tag, 0);
			//return the data from L2 written to L1
			return;
		}
	}
	// hit in l1
	else {
		//return the data
		return;
	}
}

void memory_fetch(unsigned int address, data_t * data){

	//check if it's writeback or writethrough	
	fetchcount++;
	if (writeback == 1){
		cache_read_WB(l1_instr, address, data);
	} else {
		cache_read_WT(l1_instr, address, data);
	}
}

void memory_read(unsigned int address, data_t *data)
{
	
	//check if it's writeback or writethrough
	readcount++;
	if (writeback == 1){
		cache_read_WB(l1_data, address, data);
	} else {
		cache_read_WT(l1_data, address, data);
	}

	
}
void cache_write_WT(unsigned int address){

	//write to both l1 and l2 if writethrough is flagged,
	//by fetching the blocks and tags corresponding to the
	//caches set and block structures
	//then writing them to the given set

	int l1_block_tag = get_range(l1_data, address, "tag");
	int l1_set_index = get_range(l1_data, address, "index");
	check_cache(l1_data, address);
	insert_block(l1_data, l1_set_index, l1_block_tag, 0);

	int l2_block_tag = get_range(l2_unif, address, "tag");
	int l2_set_index = get_range(l2_unif, address, "index");
	check_cache(l2_unif, address);
	insert_block(l2_unif, l2_set_index, l2_block_tag, 0);
}

void cache_write_WB(unsigned int address){

	//write to l1, if WriteBack is flagged
	//check if the current block on that address is dirty
	//if it's dirty it needs to be written up/down/out to L2 cache
	//by fetching the blocks and tags corresponding to the
	//caches set and block structures
	//then writing them to the given set

	int l1_block_tag = get_range(l1_data, address, "tag");
	int l1_set_index = get_range(l1_data, address, "index");
	age_inc(l1_data);

	if(check_dirtyblock(l1_data, l1_set_index)){
		int l2_block_tag = get_range(l2_unif, address, "tag");
		int l2_set_index = get_range(l2_unif, address, "index");

		//unsure about this one
		//check_cache(l2_unif, address);
		age_inc(l2_unif);

		insert_block(l2_unif, l2_set_index, l2_block_tag, 0);
	}

	insert_block(l1_data, l1_set_index, l1_block_tag, 1);

}

void memory_write(unsigned int address, data_t *data)
{
	instr_count++;
	writecount++;

	if (writeback == 1){
		cache_write_WB(address);
	} else {
		cache_write_WT(address);
	}

}

void del_memory(cache_t *cache){
	//iterate over each set and each block to free every mallocated variable
	int i, j;
	for (i=0; i < cache->numsets; i++){
		for (j=0; j < cache->associativity; j++){
			free(cache->set[i].block[j].data);	
		}
		free(cache->set[i].block);
	}
	free(cache->set);
	free(cache);
}

void memory_finish(void)
{
	fprintf(stdout, "Executed %lu instructions.\n\n", instr_count);
	fprintf(stdout, "Executed %d fetches.\n\n", fetchcount);
	fprintf(stdout, "Executed %f was fetches.\n\n", (double)((double)fetchcount/(double)instr_count));

	fprintf(stdout, "Executed %d reads.\n", readcount);
	fprintf(stdout, "Executed %f was reads.\n\n", (double)((double)readcount/(double)instr_count));

	fprintf(stdout, "Executed %d writes.\n", writecount);
	fprintf(stdout, "Executed %f was writes.\n\n", (double)((double)writecount/(double)instr_count));

	fetchcount = 0;
	readcount = 0;
	writecount = 0;




	
	/* Deinitialize memory subsystem here */

	double l1_instr_missrate = 1 - (double)((double)l1_instr->hit/(double)(l1_instr->hit+l1_instr->miss));
	printf("l1_instr cache hits:\t%d\t\n",l1_instr->hit);
	printf("l1_instr cache misses: \t%d\t\n",l1_instr->miss);
	printf("l1_instr miss ratio: \t%f\n", l1_instr_missrate);
	double l1_instr_amat = 1 + (l1_instr_missrate * l1misspenalty);
	printf("l1_instr AMAT: \t\t%f\n\n", l1_instr_amat);

	double l1_data_missrate = 1 - (double)((double)l1_data->hit/(double)(l1_data->hit+l1_data->miss));
	printf("l1_data cache hits: \t%d\t\n",l1_data->hit);
	printf("l1_data cache misses: \t%d\t\n",l1_data->miss);
	printf("l1_data miss ratio: \t%f\n", l1_data_missrate);
	double l1_data_amat = 1 + (l1_data_missrate * l1misspenalty);
	printf("l1_data AMAT: \t\t%f\n\n", l1_data_amat);

	double l2_unif_missrate = 1 - (double)((double)l2_unif->hit/(double)(l2_unif->hit+l2_unif->miss));
	printf("l2_unif cache hits:\t%d\t\n",l2_unif->hit);
	printf("l2_unif cache misses: \t%d\t\n",l2_unif->miss);
	printf("l2_unif missratio: \t%f\n", l2_unif_missrate);
	double l2_unif_amat = 1 + (l2_unif_missrate * l2misspentaly);
	printf("l2_unif AMAT: \t\t%f\n\n", l2_unif_amat);

	printf("global miss ratio \t%f\n",(double)(l2_unif->miss/(double)(l1_instr->hit+l1_instr->miss+l1_data->hit+l1_data->miss)));
	printf("total average memory access time is %f\n", ((l1_instr_amat + l1_data_amat)/2)+l2_unif_amat);


	del_memory(l1_instr);
	del_memory(l1_data);
	del_memory(l2_unif);
	
	
}

