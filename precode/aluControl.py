from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class AluControl(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'AluControl should have two input'
        assert(len(outputValueNames) == 0), 'AluControl has only one output'
        assert(len(control) == 1), 'AluControl has no control signal'
        assert(len(outputSignalNames) == 1), 'AluControl does not have any control output'

        self.inputZero = inputSources[0][1]
        self.ctrlALUOp = control[0][1]
        self.controlZero = outputSignalNames[0]

    def writeOutput(self):
        pass

    def setControlSignals(self):
        func = self.inputValues[self.inputZero]
        ALUOp = self.controlSignals[self.ctrlALUOp]

        assert(type(ALUOp) == int)
        assert( ALUOp == 0 or
                ALUOp == 1 or
                ALUOp == 2 or
                ALUOp == 3)
        # LW / SW
        if ALUOp == 0:
            self.outputControlSignals[self.controlZero] = 2
            return
        # BEQ
        elif ALUOp == 1:
            self.outputControlSignals[self.controlZero] = 6
            return
        # R-Format
        elif ALUOp == 2:
            assert(type(func) == long)
            '''assert( func == 32 or
                    func == 34 or
                    func == 36 or
                    func == 37 or
                    func == 42)'''
            # Add
            if func == 32 or func == 0 or func == 33:
                self.outputControlSignals[self.controlZero] = 2

            # Subtract
        elif func == 34 or funct == 35:
                self.outputControlSignals[self.controlZero] = 6

            # AND
            elif func == 36:
                self.outputControlSignals[self.controlZero] = 0

            # OR
            elif func == 37:
                self.outputControlSignals[self.controlZero] = 1

            # Set on Less than
            elif func == 42:
                self.outputControlSignals[self.controlZero] = 7
            return

        # BNE
        elif ALUOp == 3:
            self.outputControlSignals[self.controlZero] = 15

class TestALU(unittest.TestCase):
    def setUp(self):
        self.testALUControl = AluControl()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["data1"],
            [],
            ["signal"]
        )

        self.testALUControl.connect(
            [],
            [(self.testinput, "data1")],
            [(self.testinput, "signal")],
            ["output"]
        )

        self.testoutput.connect(
            [],
            [],
            [(self.testALUControl, "output")],
            []
        )

    def test_correct_behaviour(self):
        def setvar(func, ALUOp, expected):
            self.testinput.setOutputValue("data1", func)
            self.testinput.setOutputControl("signal", ALUOp)

            self.testALUControl.readInput()
            self.testALUControl.readControlSignals()
            self.testALUControl.setControlSignals()

            self.testoutput.readInput()
            self.testoutput.readControlSignals()

            output = self.testoutput.controlSignals["output"]
            self.assertEqual(output, expected)

        # LW (if LW works SW will work as they have the exact same code)
        setvar(32, 0, 2)
        # Branch Equal
        setvar(32, 1, 6)
        # R-type add
        setvar(32, 2, 2)
        # R-type sub
        setvar(34, 2, 6)
        # R-type AND
        setvar(36, 2, 0)
        # R-type OR
        setvar(37, 2, 1)
        # R-type sett on less than
        setvar(42, 2, 7)


    def assert_callback(self, arg0, arg1, arg2):
        self.testinput.setOutputValue("data1", arg0)
        self.testinput.setOutputControl("signal", arg1)

        self.testALUControl.readInput()
        self.testALUControl.readControlSignals()
        self.testALUControl.setControlSignals()

        self.testoutput.readInput()

        output = self.testoutput.controlSignals["output"]
        self.assertEqual(output, arg2)

    def test_incorrect_behaviour(self):
        #testing ALUOp
        self.assertRaises(AssertionError, self.assert_callback, 32, long(0), 2)
        self.assertRaises(AssertionError, self.assert_callback, 32, str(0), 2)
        self.assertRaises(AssertionError, self.assert_callback, 32, 5, 2)

        #testing Func code
        self.assertRaises(AssertionError, self.assert_callback, long(32), 2, 2)
        self.assertRaises(AssertionError, self.assert_callback, str(32), 2, 2)
        self.assertRaises(AssertionError, self.assert_callback, 31, 2, 2)

if __name__ == '__main__':
    unittest.main()
