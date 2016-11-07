'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
import common
from testElement import TestElement


class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}

        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect Register to input sources and controller

        Note that the first inputSource is input zero, and the second is input 1
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 4), 'Register should have 4 inputs'
        assert(len(outputValueNames) == 2), 'Register should have 2 output'
        assert(len(control) == 1), 'Register has one control signal'
        assert(len(outputSignalNames) == 0), 'Mux does not have any control output'

        self.inputRegister1 = inputSources[0][1]
        self.inputRegister2 = inputSources[1][1]
        self.inputWregister = inputSources[2][1]
        self.inputWdata = inputSources[3][1]
        self.outputReg1 = outputValueNames[0]
        self.outputReg2 = outputValueNames[1]
        self.controlWrt = control[0][1]

    def writeOutput(self):
        reg1 = self.inputValues[self.inputRegister1]
        reg2 = self.inputValues[self.inputRegister2]
        wreg = self.inputValues[self.inputWregister]
        wdat = self.inputValues[self.inputWdata]
        ctrl = self.controlSignals[self.controlWrt]
        

        self.outputValues[self.outputReg1] = self.register[reg1]
        self.outputValues[self.outputReg2] = self.register[reg2]


        if ctrl:
            if wreg == 0L:
                return
            self.register[wreg] = wdat
            return


    def printAll(self):
        '''
        Print the name and value in each register.
        '''

        # Note that we won't actually use all the registers listed here...
        registerNames =  ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                            '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                            '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                            '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

        print
        print "Register file"
        print "================"
        for i in range(0, 32):
            print    "%s \t=> %s (%s)" % (registerNames[i], common.fromUnsignedWordToSignedWord(self.register[i]), hex(long(self.register[i]))[:-1])
        print "================"
        print
        print

class TestRegisterFile(unittest.TestCase):
    def setUp(self):
        self.testReg = RegisterFile()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["addr1", "addr2", "dest", "data"],
            [],
            ["signal"]
        )

        self.testReg.connect(
            [(self.testinput, "addr1"),
            (self.testinput, "addr2"),
            (self.testinput, "dest"),
            (self.testinput, "data")],
            ["data1", "data2"],
            [(self.testinput, "signal")],
            []
        )

        self.testoutput.connect(
            [(self.testReg, "data1"), (self.testReg, "data2")],
            [],
            [],
            []
        )
    def setvar(self, addr1, addr2, dest, data, signal):
        self.testinput.setOutputValue("addr1", addr1)
        self.testinput.setOutputValue("addr2", addr2)
        self.testinput.setOutputValue("dest", dest)
        self.testinput.setOutputValue("data", data)
        self.testinput.setOutputControl("signal", signal)

        self.testReg.readInput()
        self.testReg.readControlSignals()
        self.testReg.writeOutput()

        self.testoutput.readInput()


    def test_correct_behaviour(self):
        self.setvar(1, 2, 5, 1234, 1)
        self.setvar(5, 2, 3, 4156, 1)
        self.setvar(4, 2, 5, 9942, 1)
        self.setvar(2, 2, 7, 89, 1)
        self.setvar(3, 4, 5, 1122, 1)
        self.setvar(7, 2, 2, 1550, 1)
        #self.testReg.printAll()



if __name__ == '__main__':
    unittest.main()
