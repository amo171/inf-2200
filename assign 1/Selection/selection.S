/** @file fib.S
 *  @brief Selection sort for signed integers written in x86 AT&T assembly.
 *
 *  @author Erlend Graff <erlend.h.graff@uit.no>
 */

#include "asmdef.h"

########### Make function 'selection_sort' visible as global symbol ###########
DECLARE_GLOBAL(selection_sort)


FUNC(selection_sort):
	pushl	%ebp                    # Save old stack frame
	movl	%esp, %ebp              # Create new stack frame
	
  # Save callee-saved registers EBX, ESI and EDI, so we can use them freely
	pushl	%ebx
	pushl	%esi
	pushl	%edi
	
	movl	$0, %ecx								# i = 0
	movl	8(%ebp), %ebx						# ebx = arr
	movl  12(%ebp), %edx					# edx = size
  
  # We're going to use ESI for j and EDI for tmp
	
.outer_loop:
	cmpl	%edx, %ecx							# Compare i and size
	jge		.after_outer_loop				# Break loop if (i >= size)
	
	movl	%ecx, %eax							# min = i
	movl	%ecx, %esi							# j = i
	incl	%esi										# j++
	
.inner_loop:
	cmpl	%edx, %esi							# Compare j and size
	jge		.after_inner_loop
	
	movl	(%ebx, %eax, 4), %edi		# EDI = arr[min]
	cmpl	%edi, (%ebx, %esi, 4)		# Compare arr[min] with arr[j]
	jge		.inner_next
	movl	%esi, %eax							# min = j

.inner_next:
	incl	%esi										# j++
	jmp		.inner_loop

.after_inner_loop:
	cmpl	%eax, %ecx							# Compare min and i
	je		.outer_next
	
	# Swap
	movl	(%ebx, %ecx, 4), %edi		# tmp = arr[i]
	pushl	%edx										# Save EDX
	movl	(%ebx, %eax, 4), %edx		# edx = arr[min]
	movl	%edx, (%ebx, %ecx, 4)		# arr[i] = edx
	movl	%edi, (%ebx, %eax, 4)		# arr[min] = tmp
	popl	%edx										# Restore EDX
	
.outer_next:
	incl	%ecx                    # i++
	jmp		.outer_loop
	
.after_outer_loop:
  # Restore callee-saved registers
	popl	%edi
	popl	%esi
	popl	%ebx
  
	popl	%ebp                    # Restore caller's stack frame
	ret                           # Return to caller
