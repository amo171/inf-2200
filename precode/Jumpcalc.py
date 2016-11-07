from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class JumpCalc(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'SignExtender should have two input'
        assert(len(outputValueNames) == 1), 'SignExtender has only one output'
        assert(len(control) == 0), 'SignExtender has no control signal'
        assert(len(outputSignalNames) == 0), 'SignExtender does not have any control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.outputName = outputValueNames[0]

    def writeOutput(self):
        jumpaddr = self.inputValues[self.inputZero]
        PCShift = self.inputValues[self.inputOne]

        #make jumpaddr take the seven lower bytes
        jumpaddr = jumpaddr << 2
        #mask the PC addres so that it's only the highest byte
        PCShift = PCShift & 0xf0000000

        self.outputValues[self.outputName] = jumpaddr | PCShift


class TestShift(unittest.TestCase):
    def setUp(self):
        self.testShifter = JumpCalc()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["unshifted", "bais"],
            [],
            []
        )

        self.testShifter.connect(
            [(self.testinput, "unshifted"), (self.testinput, "bais")],
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
        self.testinput.setOutputValue("unshifted", long(178956970))
        self.testinput.setOutputValue("bais", long(15))


        self.testShifter.readInput()
        self.testShifter.writeOutput()

        self.testoutput.readInput()

        output = self.testoutput.inputValues["shifted"]
        self.assertEqual(output, long(12))

if __name__ == '__main__':
    unittest.main()
