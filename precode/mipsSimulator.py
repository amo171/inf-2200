'''
Code written for inf-2200, University of Tromso
'''

from pc import PC
from add import Add
from mux import Mux
from registerFile import RegisterFile
from instructionMemory import InstructionMemory
from dataMemory import DataMemory
from constant import Constant
from randomControl import RandomControl
from wall import Wall
from signExtender import SignExtender
from leftShifter import LeftShifter
from dataMemory import DataMemory
from branch import Branch
from aluControl import AluControl
from alu import ALU
from controlelement import ControlElement
from registerFile import RegisterFile
from Jumpcalc import JumpCalc
import pdb


class MIPSSimulator():
	'''Main class for MIPS pipeline simulator.

	Provides the main method tick(), which runs pipeline

	for one clock cycle.
	'''
	def __init__(self, memoryFile):
		self.nCycles = 0 # Used to hold number of clock cycles spent executing instructions

		# Fetch
		self.PCMux	  = Mux()
		self.ProgramC   = PC(long(0xbfc00200))
		self.InstMem	= InstructionMemory(memoryFile)
		self.IFadder	= Add()
		self.JMux	   = Mux()
		self.IFaddconst = Constant(4)
		self.IF_ID_Wall = Wall()
		self.fetchgroup = {}

		# Decode
		self.register   = RegisterFile()
		self.signext	= SignExtender()
		self.control	= ControlElement()
		self.jmpCalc	= JumpCalc()
		self.ID_EX_Wall = Wall()

		# Execute
		self.EXadder	= Add()
		self.shiftL	 = LeftShifter()
		self.ALogicUnit = ALU()
		self.ALUSrcMux  = Mux()
		self.RegDstMux  = Mux()
		self.ALUctrl	= AluControl()
		self.EX_MEM_Wall= Wall()

		# Memory
		self.storage	= DataMemory(memoryFile)
		self.brnch	  = Branch()
		self.MEM_WB_Wall= Wall()

		# Write Back
		self.WBmux = Mux()

		self.ProgramC
		self.elements1 = [self.InstMem, self.IFaddconst, self.IFadder, self.PCMux, self.JMux]
		self.elements2 = [self.control, self.register, self.signext, self.jmpCalc]
		self.elements3 = [self.shiftL, self.ALUSrcMux, self.RegDstMux, self.ALUctrl, self.ALogicUnit, self.EXadder]
		self.elements4 = [self.brnch, self.storage]
		self.elementsboot = [self.IFaddconst, self.IFadder, self.InstMem,
							 self.IF_ID_Wall, self.register, self.signext, self.control, self.jmpCalc,
							 self.ID_EX_Wall, self.RegDstMux, self.shiftL, self.EXadder, self.ALUSrcMux, self.ALUctrl, self.ALogicUnit,
							 self.EX_MEM_Wall, self.brnch, self.storage,
							 self.MEM_WB_Wall, self.WBmux, self.PCMux, self.JMux]
		self.walls = [self.MEM_WB_Wall, self.EX_MEM_Wall, self.ID_EX_Wall, self.IF_ID_Wall]


		self._connectCPUElements()

	def _connectCPUElements(self):
		# IF
		self.PCMux.connect(
			[(self.IFadder, "adderout"), (self.EX_MEM_Wall, "adderoutput")],
			["PCmuxoutput"],
			[(self.brnch, "PCSrc")],
			[]
		)

		self.JMux.connect(
			[(self.PCMux, "PCmuxoutput"), (self.jmpCalc, "output")],
			["output"],
			[(self.control, "Jump")],
			[]
		)

		self.IFaddconst.connect(
			[],
			['constant'],
			[],
			[]
		)

		self.ProgramC.connect(
			[(self.JMux, "output")],
			["output"],
			[],
			[]
		)

		self.InstMem.connect(
			[(self.ProgramC, "output")],
			["opcode", "rs", "rt", "rd", "shamt", "funct", "imm", "addr"],
			[],
			[]
		)

		self.IFadder.connect(
			[(self.ProgramC, "output"), (self.IFaddconst, "constant")],
			["adderout"],
			[],
			[]
		)

		self.IF_ID_Wall.connect(
			[(self.InstMem, "opcode"),(self.InstMem, "rs"),
			(self.InstMem, "rt"),(self.InstMem, "rd"),
			(self.InstMem, "shamt"), (self.InstMem, "funct"),
			(self.InstMem, "imm"), (self.InstMem, "addr"),
			(self.IFadder, "adderout")],
			["opcode", "rs", "rt", "rd",
			 "shamt", "funct", "imm", "addr",
			 "adderout"],
			[],
			[]
		)
		# IF
		# ID
		self.register.connect(
			[(self.IF_ID_Wall, "rs"), (self.IF_ID_Wall, "rt"),
			 (self.MEM_WB_Wall, "regdstoutput"), (self.WBmux, "output")],
			["Reg1", "Reg2"],
			[(self.MEM_WB_Wall, "RegWrite")],
			[]
		)

		self.signext.connect(
			[(self.IF_ID_Wall, "imm")],
			["extended"],
			[],
			[]
		)

		self.control.connect(
			[(self.IF_ID_Wall, "opcode")],
			[],
			[],
			["RegDst", "RegWrite", "ALUSrc", "MemtoReg",
			 "MemWrite", "MemRead", "Branch", "ALUOp", "Jump"]
		)

		self.jmpCalc.connect(
			[(self.IF_ID_Wall, "addr"), (self.IF_ID_Wall, "adderout")],
			["output"],
			[],
			[]
		)

		self.ID_EX_Wall.connect(
			[(self.register, "Reg1"), (self.register, "Reg2"),
			(self.signext, "extended"), (self.jmpCalc, "output"),
			(self.IF_ID_Wall, "adderout"), (self.IF_ID_Wall, "funct"),
			(self.IF_ID_Wall, "rd"), (self.IF_ID_Wall, "addr"),
			(self.IF_ID_Wall, "rt")],
			["Reg1", "Reg2", "extended", "output",
			 "adderout", "funct", "rd", "addr", "rt"],
			[(self.control, "RegDst"), (self.control, "RegWrite"),
			(self.control, "ALUSrc"), (self.control, "MemtoReg"),
			(self.control, "MemWrite"), (self.control, "MemRead"),
			(self.control, "Branch"), (self.control, "ALUOp"),
			(self.control, "Jump")],
			["RegDst", "RegWrite", "ALUSrc", "MemtoReg",
			 "MemWrite", "MemRead", "Branch", "ALUOp", "Jump"]
		)
		#ID
		#EX

		self.EXadder.connect(
			[(self.ID_EX_Wall, "adderout"), (self.shiftL, "shifted")],
			["output"],
			[],
			[]
		)

		self.shiftL.connect(
			[(self.ID_EX_Wall, "extended")],
			["shifted"],
			[],
			[]
		)

		self.ALogicUnit.connect(
			[(self.ID_EX_Wall, "Reg1"), (self.ALUSrcMux, "output")],
			["result"],
			[(self.ALUctrl, "ALUctrlsig")],
			["zero"]
		)

		self.ALUSrcMux.connect(
			[(self.ID_EX_Wall, "Reg2"), (self.ID_EX_Wall, "extended")],
			["output"],
			[(self.ID_EX_Wall, "ALUSrc")],
			[]
		)

		self.RegDstMux.connect(
			[(self.ID_EX_Wall, "rt"), (self.ID_EX_Wall, "rd")],
			["RegDstoutput"],
			[(self.ID_EX_Wall, "RegDst")],
			[]
		)

		self.ALUctrl.connect(
			[(self.ID_EX_Wall, "funct")],
			[],
			[(self.ID_EX_Wall, "ALUOp")],
			["ALUctrlsig"]
		)

		self.EX_MEM_Wall.connect(
			[(self.EXadder, "output"), (self.ALogicUnit, "result"),
			 (self.ID_EX_Wall, "rt"), (self.RegDstMux, "RegDstoutput")],
			["adderoutput", "result", "rt", "regdstoutput"],
			[(self.ID_EX_Wall, "RegWrite"), (self.ID_EX_Wall, "MemtoReg"),
			 (self.ID_EX_Wall, "MemWrite"), (self.ID_EX_Wall, "MemRead"),
			 (self.ID_EX_Wall, "Branch"), (self.ALogicUnit, "zero")],
			["RegWrite", "MemtoReg", "MemWrite", "MemRead", "Branch", "zero"]
		)
		#EX
		#MEM

		self.storage.connect(
			[(self.EX_MEM_Wall, "result"), (self.EX_MEM_Wall, "rt")],
			["data"],
			[(self.EX_MEM_Wall, "MemWrite"), (self.EX_MEM_Wall, "MemRead")],
			[]
		)

		self.brnch.connect(
			[],
			[],
			[(self.EX_MEM_Wall, "Branch"), (self.EX_MEM_Wall, "zero")],
			["PCSrc"]
		)


		self.MEM_WB_Wall.connect(
			[(self.EX_MEM_Wall, "adderoutput"), (self.storage, "data"),
			 (self.EX_MEM_Wall, "regdstoutput")],
			["adderoutput", "data", "regdstoutput"],
			[(self.EX_MEM_Wall, "RegWrite"), (self.EX_MEM_Wall, "MemtoReg")],
			["RegWrite", "MemtoReg"]
		)
		#MEM
		#WB
		self.WBmux.connect(
			[(self.MEM_WB_Wall, "adderoutput"), (self.MEM_WB_Wall, "data")],
			["output"],
			[(self.MEM_WB_Wall, "MemtoReg")],
			[]
		)

	def clockCycles(self):
		'''Returns the number of clock cycles spent executing instructions.'''

		return self.nCycles

	def dataMemory(self):
		'''Returns dictionary, mapping memory addresses to data, holding
		data memory after instructions have finished executing.'''

		return self.dataMemory.memory

	def registerFile(self):
		'''Returns dictionary, mapping register numbers to data, holding
		register file after instructions have finished executing.'''

		return self.registerFile.register

	def printDataMemory(self):
		self.dataMemory.printAll()

	def printRegisterFile(self):
		self.registerFile.printAll()

	def bootup(self):
		self.ProgramC.writeOutput()

		for elem in self.elementsboot:
			elem.readControlSignals()
			elem.readInput()
			elem.writeOutput()
			elem.setControlSignals()

		self.ProgramC.readInput()


	def tick(self):
		'''Execute one clock cycle of pipeline.'''

		self.nCycles += 1
		

		self.ProgramC.writeOutput()

		for elem in self.walls:
			elem.writeOutput()
			elem.setControlSignals()

		self.WBmux.readControlSignals()
		self.WBmux.readInput()
		self.WBmux.writeOutput()
		self.WBmux.setControlSignals()

		for elem in self.elements4:
			elem.readControlSignals()
			elem.readInput()
			elem.writeOutput()
			elem.setControlSignals()

		for elem in self.elements3:
			elem.readControlSignals()
			elem.readInput()
			elem.writeOutput()
			elem.setControlSignals()

		for elem in self.elements2:
			elem.readControlSignals()
			elem.readInput()
			elem.writeOutput()
			elem.setControlSignals()

		for elem in self.elements1:
			elem.readControlSignals()
			elem.readInput()
			elem.writeOutput()
			elem.setControlSignals()

		for elem in self.walls:
			elem.readControlSignals()
			elem.readInput()

		self.register.printAll()
		self.ProgramC.readInput()
		print "number of cycles", self.nCycles, "\n"
