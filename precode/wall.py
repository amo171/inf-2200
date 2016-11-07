from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class Wall(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == len(outputValueNames)), 'Wall must the same amount of inputs as outputs'
        assert(len(control) == len(outputSignalNames)), 'Wall must the same amount of control signals as countrol output signals'

        self.inputSources = inputSources
        self.control = control
    def readInput(self):
        #pass through any inputs straight through
        for inputs in self.inputSources:
            src, name = inputs
            self.outputValues[name] = src.getOutputValue(name)

    def writeOutput(self):
        pass

    def readControlSignals(self):
        #pass through any signals straight through
        for controls in self.control:
            src, name = controls
            self.outputControlSignals[name] = src.getControlSignal(name)

    def setControlSignals(self):
        pass
