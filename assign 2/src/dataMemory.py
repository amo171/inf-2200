'''
Implements CPU element for Data Memory in MEM stage.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
from memory import Memory
import common
from testElement import TestElement
import unittest

class DataMemory(Memory):
    def __init__(self, filename="add.mem"):
        Memory.__init__(self, filename)

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        '''
        Connect Memory to input sources and controller

        Note that the first inputSource is input zero, and the second is input 1
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Memory should have two input'
        assert(len(outputValueNames) == 1), 'Memory has only one output'
        assert(len(control) == 2), 'Memory has no control signal'
        assert(len(outputSignalNames) == 0), 'Memory does not have any control output'

        self.inputAddr = inputSources[0][1]
        self.inputwdat = inputSources[1][1]
        self.outputRdat = outputValueNames[0]
        self.ctrlMemWrt = control[0][1]
        self.ctrlMemRed = control[1][1]

    def writeOutput(self):
        address = self.inputValues[self.inputAddr]
        wdat = self.inputValues[self.inputwdat]
        MemWrt = self.controlSignals[self.ctrlMemWrt]
        MemRed = self.controlSignals[self.ctrlMemRed]

        print "datmem addr is\t", hex(address)
        print "datmem wdat is\t", wdat
        print "datmem MemW is\t", MemWrt
        print "datmem memR is\t", MemRed

        assert(type(address) == long)
        #assert(type(wdat) == long)
        assert(type(MemWrt) == int)
        assert(type(MemRed) == int)

        if MemRed and MemWrt:
            raise(AssertionError)

        if MemWrt:
            self.memory[address] = wdat
            return

        if MemRed:
            self.outputValues[self.outputRdat] = self.memory[address]
            return



class TestDatMem(unittest.TestCase):
    def setUp(self):
        self.testmem = DataMemory()
        self.testInput = TestElement()
        self.testOutput = TestElement()
        self.testInput.connect(
        [],
        ["dataR", "dataW"],
        [],
        ["writesignal", "readsignal"]
        )
        self.testmem.connect(
        [(self.testInput, "dataR"), (self.testInput, "dataW")],
        ["output"],
        [(self.testInput, "writesignal"), (self.testInput, "readsignal")],
        []
        )
        self.testOutput.connect(
        [(self.testmem, "output")],
        [],
        [],
        []
        )


    def test_correct_behavior(self):
        def setup(read, write):
            self.testInput.setOutputControl("readsignal", read)
            self.testInput.setOutputControl("writesignal", write)

            self.testmem.readInput()
            self.testmem.readControlSignals()
            self.testmem.writeOutput()

            self.testOutput.readInput()

        self.testInput.setOutputValue("dataR", long(0xbfc00000))
        self.testInput.setOutputValue("dataW", long(15))

        setup(1, 0)

        output = self.testOutput.inputValues["output"]
        self.assertEqual(output, long(0x0bf00080))


        self.testInput.setOutputValue("dataR", long(0xbfc00000))
        self.testInput.setOutputValue("dataW", long(7))

        setup(0, 1)

        setup(1, 0)

        output = self.testOutput.inputValues["output"]
        self.assertEqual(output, long(7))

    def assert_callback(self, arg1, arg2):
        self.testInput.setOutputValue("dataR", long(0xbfc00000))
        self.testInput.setOutputValue("dataW", long(15))
        self.testInput.setOutputControl("readsignal", arg1)
        self.testInput.setOutputControl("writesignal", arg2)

        self.testmem.readInput()
        self.testmem.readControlSignals()
        self.testmem.writeOutput()

    def test_incorrect_behaviour(self):

        self.assertRaises(AssertionError, self.assert_callback, 1, 1)



if __name__ == '__main__':
    unittest.main()
