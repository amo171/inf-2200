'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class Memory(CPUElement):
    def __init__(self, filename):

        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'long'

        self.memory = {}

        self.initializeMemory(filename)

    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''
        with open(filename, "r") as f:
            for data in f:
                if data.startswith('#') or data.startswith('\n'):
                    continue
                data = data.split('\t')
                addr = long(data[0], 0)
                instr = long(data[1], 0)

                self.memory[addr] = instr



    def printAll(self):
        for key in sorted(self.memory.iterkeys()):
            print "%s\t=> %s\t(%s)" % (hex(long(key))[:-1], common.fromUnsignedWordToSignedWord(self.memory[key]), hex(long(self.memory[key]))[:-1])

class TestMem(unittest.TestCase):
    def setUp(self):
        self.testmem = Memory("selectionsort.mem")
        self.testmem.initializeMemory("selectionsort.mem")

    def test_entry(self):
        testarray = ["0xbfc00100", "0xbfc00124", "0xbfc0012c", "0xbfc00158"]
        for entry in testarray:
            self.assertTrue(self.testmem.memory[long(entry, 0)])




if __name__ == '__main__':
    unittest.main()
