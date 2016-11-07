'''
Implement a CPU-element for holding a single integer constant.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement

class Constant(CPUElement):
    '''
    Element that always output a constant value.
    '''
    def __init__(self, constant):
        '''
        Constructor.

        @param constant that is always output by this element
        '''
        self.constantValue = constant

    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), 'Constants have no input'
        assert(len(outputValueNames) == 1), 'Constants has only one output'
        assert(len(control) == 0), 'Constants do not have any control signal'
        assert(len(outputSignalNames) == 0), 'Constants do not have any control output'

        self.outputName = outputValueNames[0]

    def writeOutput(self):
        self.outputValues[self.outputName] = self.constantValue
