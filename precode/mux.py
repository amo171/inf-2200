'''
Code written for inf-2200, University of Tromso
'''

import unittest
from cpuElement import CPUElement
from testElement import TestElement

class Mux(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        '''
        Connect mux to input sources and controller

        Note that the first inputSource is input zero, and the second is input 1
        '''
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Mux should have two inputs'
        assert(len(outputValueNames) == 1), 'Mux has only one output'
        assert(len(control) == 1), 'Mux has one control signal'
        assert(len(outputSignalNames) == 0), 'Mux does not have any control output'

        self.inputZero = inputSources[0][1]
        self.inputOne = inputSources[1][1]
        self.outputName = outputValueNames[0]
        self.controlName = control[0][1]

    def writeOutput(self):
        muxControl = self.controlSignals[self.controlName]

        assert(isinstance(muxControl, int))
        assert(not isinstance(muxControl, bool)) #...    (not bool)
        assert(muxControl == 0 or muxControl == 1), 'Invalid mux control signal value: %d' % (muxControl,)

        if muxControl == 0:
            self.outputValues[self.outputName] = self.inputValues[self.inputZero]
            print "mux sent from 0"
            print hex(self.inputValues[self.inputZero]), self.inputZero, "\n"
        else: # muxControl == 1
            self.outputValues[self.outputName] = self.inputValues[self.inputOne]
            print "mux sent from 1"
            print hex(self.inputValues[self.inputOne]), self.inputOne, "\n"


    def printOutput(self):
        '''
        Debug function that prints the output value
        '''
        print 'mux.output = %d' % (self.outputValues[self.outputName],)


class TestMux(unittest.TestCase):
    def setUp(self):
        self.mux = Mux()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
            [],
            ['dataA', 'dataB'],
            [],
            ['muxControl']
        )

        self.mux.connect(
            [(self.testInput, 'dataA'), (self.testInput, 'dataB')],
            ['muxData'],
            [(self.testInput, 'muxControl')],
            []
        )

        self.testOutput.connect(
            [(self.mux, 'muxData')],
            [],
            [],
            []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('dataA', 10)
        self.testInput.setOutputValue('dataB', 20)

        self.testInput.setOutputControl('muxControl', 0)

        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']

        self.assertEqual(output, 10)

        self.testInput.setOutputControl('muxControl', 1)

        self.mux.readInput()
        self.mux.readControlSignals()
        self.mux.writeOutput()
        self.testOutput.readInput()
        output = self.testOutput.inputValues['muxData']

        self.assertEqual(output, 20)

    def assert_callback(self, arg):
        self.testInput.setOutputControl('muxControl', arg)
        self.mux.readControlSignals()
        self.mux.writeOutput()

    def test_assert_on_incorrect_input(self):
        self.testInput.setOutputValue('dataA', 10)
        self.testInput.setOutputValue('dataB', 20)
        self.mux.readInput()

        self.assertRaises(AssertionError, self.assert_callback, '1')
        self.assertRaises(AssertionError, self.assert_callback, '0')
        self.assertRaises(AssertionError, self.assert_callback, True)
        self.assertRaises(AssertionError, self.assert_callback, False)

if __name__ == '__main__':
    unittest.main()
