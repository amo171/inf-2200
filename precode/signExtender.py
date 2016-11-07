from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class SignExtender(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'SignExtender should have two input'
        assert(len(outputValueNames) == 1), 'SignExtender has only one output'
        assert(len(control) == 0), 'SignExtender has no control signal'
        assert(len(outputSignalNames) == 0), 'SignExtender does not have any control output'

        self.inputZero = inputSources[0][1]
        self.outputName = outputValueNames[0]


    def writeOutput(self):
        sign = self.inputValues[self.inputZero]
        common.fromUnsignedWordToSignedWord(sign)
        sign = long(sign)
        assert(type(sign) == long)

        # match the highest bit of the sign
        # and fill the upper bits with that bit
        if sign < 0:
            sign = sign | 0xffff0000
        else:
            sign = sign | 0x00000000

        self.outputValues[self.outputName] = sign

class testSE(unittest.TestCase):
    def setUp(self):
        self.testSE = SignExtender()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["signin"],
            [],
            []
        )

        self.testSE.connect(
            [(self.testinput, "signin")],
            ["signout"],
            [],
            []
        )

        self.testoutput.connect(
            [(self.testSE, "signout")],
            [],
            [],
            []
        )

    def test_correct_behaviour(self):
        self.testinput.setOutputValue("signin", long(4))

        self.testSE.readInput()
        self.testSE.writeOutput()

        self.testoutput.readInput()

        output = self.testoutput.inputValues["signout"]
        self.assertEqual(output, 0b00000000000000000000000000000100)

        self.testinput.setOutputValue("signin", long(-4))

        self.testSE.readInput()
        self.testSE.writeOutput()

        self.testoutput.readInput()

        output = self.testoutput.inputValues["signout"]
        self.assertEqual(output, common.fromUnsignedWordToSignedWord(0b11111111111111111111111111111100))

if __name__ == '__main__':
    unittest.main()
