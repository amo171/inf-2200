from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class LeftShifter(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'SignExtender should have two input'
        assert(len(outputValueNames) == 1), 'SignExtender has only one output'
        assert(len(control) == 0), 'SignExtender has no control signal'
        assert(len(outputSignalNames) == 0), 'SignExtender does not have any control output'

        self.inputZero = inputSources[0][1]
        self.outputName = outputValueNames[0]


    def writeOutput(self):

        shiftee = self.inputValues[self.inputZero]

        shiftee = shiftee << 2

        self.outputValues[self.outputName] = shiftee

class TestShift(unittest.TestCase):
    def setUp(self):
        self.testShifter = LeftShifter()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["unshifted"],
            [],
            []
        )

        self.testShifter.connect(
            [(self.testinput, "unshifted")],
            ["shifted"],
            [],
            []
        )

        self.testoutput.connect(
            [(self.testShifter, "shifted")],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        self.testinput.setOutputValue("unshifted", long(3))

        self.testShifter.readInput()
        self.testShifter.writeOutput()

        self.testoutput.readInput()

        output = self.testoutput.inputValues["shifted"]
        self.assertEqual(output, long(12))

if __name__ == '__main__':
    unittest.main()
