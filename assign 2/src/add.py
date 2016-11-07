'''
Implements a simple CPU element for adding two integer operands.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement

class Add(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), 'Adder should have two inputs'
        assert(len(outputValueNames) == 1), 'Adder has only one output'
        assert(len(control) == 0), 'Adder should not have any control signal'
        assert(len(outputSignalNames) == 0), 'Adder should not have any control output'

        self.outputName = outputValueNames[0]

    def writeOutput(self):
        sum = 0
        for k in self.inputValues:
            print "addervalue",k,"is\t", hex(self.inputValues[k])
            assert(isinstance(self.inputValues[k], int) or isinstance(self.inputValues[k], long))
            sum += self.inputValues[k]

        self.outputValues[self.outputName] = sum & 0xffffffff # Convert to 32-bit (ignore overflow)
        print "IFAdder says pcaddr is\t", hex(self.outputValues[self.outputName]), "\n"
