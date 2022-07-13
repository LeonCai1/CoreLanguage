from Core import Core
from DeclSeq import DeclSeq
from StmtSeq import StmtSeq
from Executor import Executor

class Program:
	
	def parse(self, parser):
		parser.expectedToken(Core.PROGRAM)
		parser.scanner.nextToken()
		if parser.scanner.currentToken() != Core.BEGIN:

			self.ds = DeclSeq()
			self.ds.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.END)
		parser.scanner.nextToken()
		parser.expectedToken(Core.EOS)

	def semantic(self, parser):

		parser.scopes.append([])
		parser.scopes[-1].append({})
		if self.ds != None:
			self.ds.semantic(parser)
		parser.scopes[-1].append({})
		self.ss.semantic(parser)
		parser.scopes.pop()
		
	
	def print(self):
		print("program\n", end='')
		if hasattr(self, 'ds'):
			self.ds.print(1)
		print("begin\n", end='')
		self.ss.print(1)
		print("end\n", end='')

	def execute(self, dataFileString):
		executor = Executor(dataFileString)
		if hasattr(self, 'ds'):
			self.ds.execute(executor)
		executor.pushLocalScope()
		self.ss.execute(executor)
		self.subFromGCEnd(executor)
		executor.popLocalScope()
		if executor.gc.count()!=0:
		
			i = executor.gc.count()
			while i>0:
				i-=1
				print(f"gc:{i}")

	def subFromGCEnd(self, executor) -> None:
		temp = executor.stackSpace[-1]
		for i in range(len(temp)):
			
			for id in temp[-1].keys():
				if executor.getStackOrStatic(id)!= None:
					var = executor.getStackOrStatic(id)
					if(var.type == Core.REF):
						executor.gc.subtractFromGC(id)
						executor.gc.checkZero(id)
			temp.pop()
			
