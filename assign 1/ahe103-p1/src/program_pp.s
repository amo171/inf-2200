# 1 "asm.S"
# 1 "/home/andy/Oblig/2200-oblig/assign 1/ahe103-p1/src//"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "/usr/include/stdc-predef.h" 1 3 4
# 1 "<command-line>" 2
# 1 "asm.S"
# 1 "asmdef.h" 1
# 2 "asm.S" 2

.globl asm_function; .type asm_function, @function


################################################################################
# name: asm_function
# action:
# in:

# out:
# modifies:
# notes:
################################################################################
asm_function:

 pushl %ebp #save stack
 movl %esp, %ebp #create stack frame

 pushl %ebx #free registers
 pushl %esi #
 pushl %edi #

 movl $2, %eax # i = 2
 movl 8(%ebp), %ebx # ebx = array
 movl 12(%ebp), %edx # edx = LIMIT


#First For loop "for (i=2, i<LIMIT, i++)"
FirstFor:
 cmpl %edx, %eax # compare i and LIMIT
 jge DoneFirst # Break loop (i >= size)

#If test "if primes[i]"
FirstIf:
 movl (%ebx, %eax, 4), %edi # tmp = array[i]
 cmpl $1, %edi # compare tmp and the integer 1
 #cmpl $1, (%ebx, %eax, 4) # is it possible to merge the two previous commands?

 jne AfterIf # tmp != int 1

 movl %eax, %esi # J = I
 addl %esi, %esi # J = I+I

#Second For loop "for (j=i, i*j<LIMIT, j++)"
SecondFor:
 cmpl %edx, %esi # Compare j TO LIMIT
 jge AfterIf # Break loop (j >= LIMIT)

 movl $0, (%ebx, %esi, 4) # set Array[J] to 0

 addl %eax, %esi #increment J counter
 jmp SecondFor #repeat SecondFor

AfterIf:

 incl %eax #increment I counter
 jmp FirstFor #repeat FirstFor

DoneFirst:

 popl %edi #pop stack in reverse order
 popl %esi #
 popl %ebx #

 mov %ebp, %esp #swap set the stackpointer to the basepointer
 popl %ebp #pop the basepointer to previous stackframe
 ret #return to the main program
