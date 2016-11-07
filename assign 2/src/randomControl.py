'''
Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import random

class RandomControl(CPUElement):
    '''
    Random control unit. It randomly sets it's output signal
    '''
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Random control does not have any inputs'
        assert(len(outputValueNames) == 0), 'Random control does not have output'
        assert(len(control) == 0), 'Random control does not have any control signals'
        assert(len(outputSignalNames) == 1), 'Random control has one control output'

        self.signalName = outputSignalNames[0]

    def writeOutput(self):
        pass # randomControl has no data output

    def setControlSignals(self):
        self.outputControlSignals[self.signalName] = random.randint(0, 1)
