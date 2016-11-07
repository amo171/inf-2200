/** @file memory.h
 *  @brief Public API of memory hierarchy.
 *  @see memory.c
 */

#ifndef MEMORY_H
#define MEMORY_H

/* data_t can be any 32-bit type, such as (unsigned long), (void *) or size_t
 * (on 32-bit x86).
 */
typedef unsigned long data_t;

/** Initialize memory hierarchy.
 */
void l1_memory_init(int cachesize, int associativity);

void L2_memory_init(int cachesize, int associativity);

void memory_init(int cachesize_l1, int blocksize_l1, int ass_l1_instr, int ass_l1_data, int cachesize_l2, int ass_l2, int blocksize_l2, int wbtag);

/** Fetch instruction at given memory address.
 *
 *  @param[in] address Memory address of instruction.
 *  @param[out] data Instruction data returned by reference.
 */
void memory_fetch(unsigned int address, data_t *data);

/** Read data from memory at given memory address.
 *
 *  @param[in] address Memory address to read from.
 *  @param[out] data Memory data returned by reference.
 */
void memory_read(unsigned int address, data_t *data);

/** Write to memory at given memory address.
 *
 *  @param[in] address Memory address to write to.
 *  @param[in] data Data to write to memory.
 */
void memory_write(unsigned int address, data_t *data);

/** Clean up and deinitialize memory hierarchy.
 */
void memory_finish (void);

#endif
