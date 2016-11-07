from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class Branch(CPUElement):

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Branch should have two input'
        assert(len(outputValueNames) == 0), 'Branch has only one output'
        assert(len(control) == 2), 'Branch has no control signal'
        assert(len(outputSignalNames) == 1), 'Branch does not have any control output'

        self.sigZero = control[0][1]
        self.sigOne = control[1][1]
        self.outZero = outputSignalNames[0]

    def writeOutput(self):
        pass

    def setControlSignals(self):
        self.outputControlSignals[self.outZero] = self.controlSignals[self.sigZero] & self.controlSignals[self.sigOne]
