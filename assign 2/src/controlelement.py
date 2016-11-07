from cpuElement import CPUElement
import common
from testElement import TestElement
import unittest

class ControlElement(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):

        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), 'Control should have two inputs'
        assert(len(outputValueNames) == 0), 'Control has only one output'
        assert(len(control) == 0), 'Control has one control signal'
        assert(len(outputSignalNames) == 9), 'Control should have one control output'

        self.inputZero = inputSources[0][1]
        self.outputZero = outputSignalNames[0]
        self.outputOne = outputSignalNames[1]
        self.outputTwo = outputSignalNames[2]
        self.outputThree = outputSignalNames[3]
        self.outputFour = outputSignalNames[4]
        self.outputFive = outputSignalNames[5]
        self.outputSix = outputSignalNames[6]
        self.outputSeven = outputSignalNames[7]
        self.outputEight = outputSignalNames[8]



    def writeOutput(self):
        pass

    def setControlSignals(self):
        instr = self.inputValues[self.inputZero]

        RegDst      = self.outputZero
        RegWrite    = self.outputOne
        ALUSrc      = self.outputTwo
        MemtoReg    = self.outputThree
        MemWrite    = self.outputFour
        MemRead     = self.outputFive
        Branch      = self.outputSix
        ALUOp       = self.outputSeven
        Jump        = self.outputEight

        if type(instr) != long:
            print type(instr)
            assert(type(instr) == long)

        assert( instr == 0 or
                instr == 2 or
                instr == 4 or
                instr == 5 or
                instr == 8 or
                instr == 9 or
                instr == 15 or
                instr == 35 or
                instr == 43
                ), "invalid input"

        # R-format
        if instr == 0:
            self.outputControlSignals[RegDst]   = 1
            self.outputControlSignals[RegWrite] = 1
            self.outputControlSignals[ALUSrc]   = 0
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 2
            self.outputControlSignals[Jump]     = 0

        # Jump
        if instr == 2:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 0
            self.outputControlSignals[ALUSrc]   = 0
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 0
            self.outputControlSignals[Jump]     = 1

        # Branch Equal
        if instr == 4:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 0
            self.outputControlSignals[ALUSrc]   = 0
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 1
            self.outputControlSignals[ALUOp]    = 1
            self.outputControlSignals[Jump]     = 0

        # Branch Not Equal
        if instr == 5:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 0
            self.outputControlSignals[ALUSrc]   = 0
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 1
            self.outputControlSignals[ALUOp]    = 4
            self.outputControlSignals[Jump]     = 0

        # Add immediate signed
        if instr == 8:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 1
            self.outputControlSignals[ALUSrc]   = 1
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 0
            self.outputControlSignals[Jump]     = 0

        # no difference from signed, only if hazard control is implemented
        # will there be a difference
        # https://en.wikipedia.org/wiki/MIPS_instruction_set#MIPS_assembly_language
        # bullet point #5

        # Add immediate unsigned
        if instr == 9:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 1
            self.outputControlSignals[ALUSrc]   = 0
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 0
            self.outputControlSignals[Jump]     = 0

        # Load upper Immediate
        if instr == 15:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 1
            self.outputControlSignals[ALUSrc]   = 1
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 3
            self.outputControlSignals[Jump]     = 0

        # Load Word
        if instr == 35:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 1
            self.outputControlSignals[ALUSrc]   = 1
            self.outputControlSignals[MemtoReg] = 1
            self.outputControlSignals[MemWrite] = 0
            self.outputControlSignals[MemRead]  = 1
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 0
            self.outputControlSignals[Jump]     = 0

        # Store Word
        if instr == 43:
            self.outputControlSignals[RegDst]   = 0
            self.outputControlSignals[RegWrite] = 0
            self.outputControlSignals[ALUSrc]   = 1
            self.outputControlSignals[MemtoReg] = 0
            self.outputControlSignals[MemWrite] = 1
            self.outputControlSignals[MemRead]  = 0
            self.outputControlSignals[Branch]   = 0
            self.outputControlSignals[ALUOp]    = 0
            self.outputControlSignals[Jump]     = 0

        print self.outputControlSignals

class TestControl(unittest.TestCase):
    def setUp(self):
        self.testControl = ControlElement()
        self.testinput = TestElement()
        self.testoutput = TestElement()
        self.testinput.connect(
            [],
            ["data1"],
            [],
            []
        )

        self.testControl.connect(
            [(self.testinput, "data1")],
            [],
            [],
            ["RegDst",  "RegWrite", "ALUSrc",
            "MemtoReg", "MemWrite", "MemRead",
            "Branch",   "ALUOp",    "Jump"]
        )

        self.testoutput.connect(
            [],
            [],
            [(self.testControl, "RegDst"), (self.testControl, "RegWrite"),
            (self.testControl, "ALUSrc"), (self.testControl, "MemtoReg"),
            (self.testControl, "MemWrite"), (self.testControl, "MemRead"),
            (self.testControl, "Branch"), (self.testControl, "ALUOp"),
            (self.testControl, "Jump")],
            []
        )

    def test_correct_behaviour(self):
        def setvar(instr, expected):
            self.testinput.setOutputValue("data1", long(instr))

            self.testControl.readInput()
            self.testControl.setControlSignals()

            self.testoutput.readControlSignals()

            RegDst = self.testoutput.controlSignals["RegDst"]
            RegWrite = self.testoutput.controlSignals["RegWrite"]
            ALUSrc = self.testoutput.controlSignals["ALUSrc"]
            MemtoReg = self.testoutput.controlSignals["MemtoReg"]
            MemWrite = self.testoutput.controlSignals["MemWrite"]
            MemRead = self.testoutput.controlSignals["MemRead"]
            Branch = self.testoutput.controlSignals["Branch"]
            ALUOp = self.testoutput.controlSignals["ALUOp"]
            Jump = self.testoutput.controlSignals["Jump"]

            self.assertEqual(RegDst, expected[0])
            self.assertEqual(RegWrite, expected[1])
            self.assertEqual(ALUSrc, expected[2])
            self.assertEqual(MemtoReg, expected[3])
            self.assertEqual(MemWrite, expected[4])
            self.assertEqual(MemRead, expected[5])
            self.assertEqual(Branch, expected[6])
            self.assertEqual(ALUOp, expected[7])
            self.assertEqual(Jump, expected[8])

        # R-Form
        setvar(0, [1,1,0,0,0,0,0,2,0])
        # Jump
        setvar(2, [0,0,0,0,0,0,0,0,1])
        # BEQ
        setvar(4, [0,0,0,0,0,0,1,1,0])
        # BNE
        setvar(5, [0,0,0,0,0,0,1,2,0])
        # ADDI
        setvar(8, [0,1,1,0,0,0,0,0,0])
        # ADDIU
        setvar(9, [0,1,0,0,0,0,0,0,0])
        # LUI
        setvar(15, [0,1,1,0,0,0,0,0,0])
        # LW
        setvar(35, [0,1,1,1,0,1,0,0,0])
        # SW
        setvar(43, [0,0,1,0,1,0,0,0,0])

    def test_incorrect_behaviour(self):
        pass

if __name__ == '__main__':
    unittest.main()
