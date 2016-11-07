'''
Implements CPU element for Instruction Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory
from testElement import TestElement
import unittest

class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'InstructionMemory should have one input'
        assert(len(outputValueNames) == 8), 'InstructionMemory has eight outputs'
        assert(len(control) == 0), 'Memory has no control signal'
        assert(len(outputSignalNames) == 0), 'Memory does not have any control output'

        self.inputZero = inputSources[0][1]
        self.outputOpcode = outputValueNames[0]
        self.outputRs = outputValueNames[1]
        self.outputRt = outputValueNames[2]
        self.outputRd = outputValueNames[3]
        self.outputShamt = outputValueNames[4]
        self.outputFunct = outputValueNames[5]
        self.outputImm = outputValueNames[6]
        self.outputAddr = outputValueNames[7]

    def writeOutput(self):
        self.address = self.inputValues[self.inputZero]

        #catch for first cycle if the PC was falsely initialized
        if self.address == 0:
            self.address = long(0xbfc00000)

        assert(type(self.address) == long)

        # split up the instruction to fit the formats
        self.outputValues[self.outputOpcode] = bit_mask(self.memory[self.address], 31, 26)
        self.outputValues[self.outputRs] = bit_mask(self.memory[self.address], 25, 21)
        self.outputValues[self.outputRt] = bit_mask(self.memory[self.address], 20, 16)
        self.outputValues[self.outputRd] = bit_mask(self.memory[self.address], 15, 11)
        self.outputValues[self.outputShamt] = bit_mask(self.memory[self.address], 10, 6)
        self.outputValues[self.outputFunct] = bit_mask(self.memory[self.address], 5, 0)
        self.outputValues[self.outputImm] = bit_mask(self.memory[self.address], 15, 0)
        self.outputValues[self.outputAddr] = bit_mask(self.memory[self.address], 25, 0)



def bit_mask(num, start, end):
	binstring = "{0:032b}".format(num)
	number = long(binstring[31-start:31-end+1], 2)
	return number


class TestInstMem(unittest.TestCase):
    def setUp(self):
        self.testmem = InstructionMemory("selectionsort.mem")
        self.testInput = TestElement()
        self.testOutput = TestElement()
        self.testInput.connect(
        [],
        ["data1"],
        [],
        []
        )
        self.testmem.connect(
        [(self.testInput, "data1")],
        ["OPcode" ,"Rs", "Rt", "Rd", "shamt", "funct", "immediate", "address"],
        [],
        []
        )
        self.testOutput.connect(
        [(self.testmem, "OPcode"), (self.testmem, "Rs"), (self.testmem, "Rt"),
        (self.testmem, "Rd"), (self.testmem, "shamt"), (self.testmem, "funct")
        ,(self.testmem, "immediate"), (self.testmem, "address")],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        # Testing the first address in selectionsort.mem
        self.testInput.setOutputValue('data1', long(0xbfc00000))

        self.testmem.readInput()
        self.testmem.writeOutput()
        # Read the input at the testoutput element
        self.testOutput.readInput()

        output = self.testOutput.inputValues['OPcode']
        self.assertEqual(output, bit_mask(0x3c10c000, 31, 26))

        output = self.testOutput.inputValues['Rs']
        self.assertEqual(output, bit_mask(0x3c10c000, 25, 21))

        output = self.testOutput.inputValues['Rt']
        self.assertEqual(output, bit_mask(0x3c10c000, 20, 16))

        output = self.testOutput.inputValues['Rd']
        self.assertEqual(output, bit_mask(0x3c10c000, 15, 11))

        output = self.testOutput.inputValues['shamt']
        self.assertEqual(output, bit_mask(0x3c10c000, 10, 6))

        output = self.testOutput.inputValues['funct']
        self.assertEqual(output, bit_mask(0x3c10c000, 5, 0))

        output = self.testOutput.inputValues['immediate']
        self.assertEqual(output, bit_mask(0x3c10c000, 15, 0))

        output = self.testOutput.inputValues['address']
        self.assertEqual(output, bit_mask(0x3c10c000, 25, 0))

if __name__ == '__main__':
    unittest.main()
