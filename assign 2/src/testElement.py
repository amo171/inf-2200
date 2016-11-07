'''
Implements a simple CPU Element that can be convenient to use in testing
of other CPU Elements.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement

class TestElement(CPUElement):
    def __init__(self):
        pass

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        self.inputNames = []
        for src, name in inputSources:
            self.inputNames.append(name)

        self.controlNames = []
        for src, name in control:
            self.controlNames.append(name)

    def setOutputValue(self, name, value):
        self.outputValues[name] = value

    def setOutputControl(self, name, value):
        self.outputControlSignals[name] = value

    def writeOutput(self):
        pass
