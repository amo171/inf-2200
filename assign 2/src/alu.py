from cpuElement import CPUElement
from memory import Memory
import common
from testElement import TestElement
import unittest

class ALU(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):

        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'ALU should have two inputs'
        assert(len(outputValueNames) == 1), 'ALU has only one output'
        assert(len(control) == 1), 'ALU has one control signal'
        assert(len(outputSignalNames) == 1), 'ALU should have one control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.outputName = outputValueNames[0]
        self.controlName = control[0][1]
        self.outputSig = outputSignalNames[0]
        self.controlflag = False

    def writeOutput(self):

        control = self.controlSignals[self.controlName]
        data0 = self.inputValues[self.inputZero]
        data1 = self.inputValues[self.inputOne]

        assert(type(control) == int)
        assert( control ==  0 or
                control ==  1 or
                control ==  2 or
                control ==  6 or
                control ==  7 or
                control == 12 or
                control == 15)

        # AND
        if control == 0:
            Res = (data0 & data1)

        # OR
        elif control == 1:
            Res = (data0 | data1)

        # Add
        elif control == 2:
            Res = data0 + data1

        # Sub
        elif control == 6:
            Res = data0 - data1

        # Set less than
        elif control == 7:
            if data0 < data1:
                Res = 1
            else:
                Res = 0
        # BNE
        elif control == 9:
            Res = 0
            if data0 != data1:
                self.controlflag = True

        # NOR
        elif control == 12:
            Res = ~(data0 | data1)
            Res *= -1
            common.fromSignedWordToUnsignedWord(Res)

        # LUI
        elif control == 15:
            Res = (common.fromSignedWordToUnsignedWord(data0) << 16) & 0xffff0000


        if Res == 0 and control != 9:
            self.controlflag = True

        self.outputValues[self.outputName] = long(Res)

    def setControlSignals(self):
        if self.controlflag:
            self.outputControlSignals[self.outputSig] = 1
        else:
            self.outputControlSignals[self.outputSig] = 0

class TestALU(unittest.TestCase):
    def setUp(self):
        self.testALU = ALU()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["data1", "data2"],
            [],
            ["signal"]
        )

        self.testALU.connect(
            [(self.testinput, "data1"), (self.testinput, "data2")],
            ["dataoutput1"],
            [(self.testinput, "signal")],
            ["output"]
        )

        self.testoutput.connect(
            [(self.testALU, "dataoutput1")],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        def setvar(data0, data1, control, expected):
            self.testinput.setOutputValue("data1", data0)
            self.testinput.setOutputValue("data2", data1)
            self.testinput.setOutputControl("signal", control)

            self.testALU.readInput()
            self.testALU.readControlSignals()
            self.testALU.writeOutput()

            self.testoutput.readInput()

            output = self.testoutput.inputValues["dataoutput1"]
            self.assertEqual(output, expected)

        # AND
        setvar(3, 5, 0, 1)
        # OR
        setvar(3, 5, 1, 7)
        # add
        setvar(3, 5, 2, 8)
        # sub
        setvar(3, 5, 6, -2)
        # set on less than
        setvar(3, 5, 7, 1)
        # NOR
        setvar(3, 5, 12, 8)

    def assert_callback(self, arg0, arg1, arg2, arg3):
        self.testinput.setOutputValue("data1", arg0)
        self.testinput.setOutputValue("data2", arg1)
        self.testinput.setOutputControl("signal", arg2)

        self.testALU.readInput()
        self.testALU.readControlSignals()
        self.testALU.writeOutput()
        self.testALU.setControlSignals()

        self.testoutput.readInput()
        self.testoutput.readControlSignals()

        output = self.testoutput.inputValues["dataoutput1"]
        self.assertEqual(output, arg3)

    def test_incorrect_behaviour(self):
        self.assertRaises(AssertionError, self.assert_callback, 3, 5, long(0), 1)
        self.assertRaises(AssertionError, self.assert_callback, 3, 5, str(0), 1)
        self.assertRaises(AssertionError, self.assert_callback, 3, 5, 56, 1)




if __name__ == '__main__':
    unittest.main()
