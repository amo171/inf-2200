'''
Implements base class from which all CPU elements inherit.

Code written for inf-2200, University of Tromso
'''

class CPUElement:
    '''
    Superclass for all elements in the datapath
    '''

    def connect(self, input, outputValueNames, control, outputSignalNames):
        '''
        Connect element to other elements.

        This function is called once per CPU Element instance during simulator initialization.

        @param input: List of input sources. Each source is defined by a
        (sourceObject, outputName) tuple, where sourceObject is an instance of
        CPUElement and outputName is a string containing the name of one of the
        output values provided by the given sourceObject.

        @param outputValueNames: List of names (given as strings) for each of the
        output values produced by the current CPUElement instance.

        @param control: List of control signal sources. Each source is defined by a
        (sourceObject, signalName) tuple, where sourceObject is an instance of
        CPUElement and signalName is a string containing the name of one of the
        output control signals provided by the given sourceObject.

        @param outputControlSignalNames: List of names (given as strings) for each of
        the output control signals produced by the current CPUElement instance.
        '''
        # List of input sources, each given as a (sourceObject, outputName) tuple.
        self.inputSources = input

        # Name -> value map of input values
        self.inputValues = {}

        # Name -> value map of output values
        self.outputValues = {}

        # List of control signal sources, each given as a (sourceObject, signalName) tuple.
        self.controlSources = control

        # Name -> value map of input control signals
        self.controlSignals = {}

        # Name -> value map of output control signals (not used unless element is a controller)
        self.outputControlSignals = {}

        for i in self.inputSources:
            # Elements in list inputSources must be tuples of length 2...
            assert(isinstance(i, tuple))
            assert(len(i) == 2)

            src, name = i # Unpack tuple

            assert(isinstance(src, CPUElement)) # ...and first element must be an instance of CPUElement
            assert(isinstance(name, str)) # ... and second element must be string

            # Cannot have two input fields with the same name
            assert(not self.inputValues.has_key(name)), 'Duplicate input value name: \'%s\' in CPU Element %s' % (name, repr(self))
            self.inputValues[name] = long(0) # Input values default to 0

        for n in outputValueNames:
            # Must be string
            assert(isinstance(n, str))

            # Cannot have two output fields with the same name
            assert(n not in self.outputValues), 'Duplicate output value name: \'%s\' in CPU Element %s' % (n, repr(self))
            self.outputValues[n] = long(0) # Output values default to 0

        for i in self.controlSources:
            # Elements in list controlSources must be tuples of length 2...
            assert(isinstance(i, tuple))
            assert(len(i) == 2)

            src, name = i # Unpack tuple

            assert(isinstance(src, CPUElement)) # ...and first element must be an instance of CPUElement
            assert(isinstance(name, str)) # ... and second element must be string

            assert(not self.controlSignals.has_key(name)), 'Duplicate input control signal name: \'%s\' in CPU Element %s' % (name, repr(self))
            self.controlSignals[name] = 0 # Set all input control signals to 0 as default

        for s in outputSignalNames:
            # Must be string
            assert(isinstance(s, str))

            # Cannot have two output control signals with the same name
            assert(s not in self.outputControlSignals), 'Duplicate output control signal name: \'%s\' in CPU Element %s' % (s, repr(self))
            self.outputControlSignals[s] = 0

    def readInput(self):
        '''
        Read and set input values for this element.

        This function is called once for each simulation step.
        '''
        for i in self.inputSources:
            src, name = i
            value = src.getOutputValue(name)
            self.inputValues[name] = value

    def readControlSignals(self):
        '''
        Read and set control signals for this element.

        This function is called once for each simulation step.
        '''
        try:
            for c in self.controlSources:
                src, name = c
                signal = src.getControlSignal(name) # Invoke getControlSignal on connected CPU Element
                self.controlSignals[name] = signal
        except AttributeError:
            raise AssertionError("CPU Element %s must be connected before trying to get output!" % (repr(self),))

    def writeOutput(self):
        '''
        Set output values based on input values and control signals

        This function is called once for each simulation step.
        '''
        raise AssertionError("writeOutput must be implemented by CPU Element %s" % (repr(self),))

    def setControlSignals(self):
        '''
        Set output control signals

        This function is called once for each simulation step.
        '''
        # Most classes do not set any control signals
        pass

    def getOutputValue(self, outputName):
        '''
        Return an output value
        @param outputName: output value to read
        '''
        hasField = True
        try:
            hasField = outputName in self.outputValues
        except AttributeError:
            raise AssertionError("Trying to access output '%s' of non-connected CPU element: %s" % (outputName, repr(self)))

        assert(hasField), "Field '%s' is not an output field of CPU element: %s" % (outputName, repr(self))

        return self.outputValues[outputName]

    def getControlSignal(self, signalName):
        '''
        Return a control signal.
        @param signalName: control signal to return
        '''
        hasSignal = True
        try:
            hasSignal = signalName in self.outputControlSignals
        except AttributeError:
            raise AssertionError("Trying to access output control signal '%s' of non-connected CPU element: %s" % (signalName, repr(self)))

        assert(hasSignal), "Field '%s' is not an output control signal of CPU element: %s" % (signalName, repr(self))

        return self.outputControlSignals[signalName]
