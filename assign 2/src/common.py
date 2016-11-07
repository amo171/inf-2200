'''This file contains small utility functions for MIPS simulator.

Code written for inf-2200, University of Tromso
Author: Erlend Graff <erlend.h.graff@uit.no>
'''

# Number conversion function
# Used by ALU slt operation and debug print to display correct numbers
def fromUnsignedWordToSignedWord(num):
    # Python hack to convert from 32 bit unsigned value to signed (using 2's complement)
    # Tests if the most significant bit (sign bit) at position 31 is present,
    # and if so, convert to negative value according to 2's complement representation
    return num if not (num & 0x80000000) else -(((~num) & 0xffffffff) + 1)

def fromSignedWordToUnsignedWord(num):
    # Convert signed 32 bit (using 2's complement) to unsigned value
    # This is simply done by removing trailing sign bits, and replacing
    # them with zeros. Since a 32 bit integer is not represented using
    # 32 bits in python, this automatically renders the value "unsigned".
    return num & 0xffffffff
