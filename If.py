from Core import Core
from Cond import Cond
import StmtSeq

class If:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.cond = Cond()
		self.cond.parse(parser)
		parser.expectedToken(Core.THEN)
		parser.scanner.nextToken()
		self.ss1 = StmtSeq.StmtSeq()
		self.ss1.parse(parser)
		if parser.scanner.currentToken() == Core.ELSE:
			parser.scanner.nextToken()
			self.ss2 = StmtSeq.StmtSeq()
			self.ss2.parse(parser)
		parser.expectedToken(Core.ENDIF)
		parser.scanner.nextToken()

	def semantic(self, parser):
		self.cond.semantic(parser)
		parser.scopes[-1].append({})
		self.ss1.semantic(parser)
		parser.scopes[-1].pop()
		if hasattr(self, 'ss2'):
			parser.scopes[-1].append({})
			self.ss2.semantic(parser)
			parser.scopes[-1].pop()
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("if ", end='')
		self.cond.print()
		print(" then\n", end='')
		self.ss1.print(indent+1)
		if hasattr(self, 'ss2'):
			for x in range(indent):
				print("  ", end='')
			print("else\n", end='')
			self.ss2.print(indent+1)
		for x in range(indent):
			print("  ", end='')
		print("endif\n", end='')

	def execute(self, executor):
		condition = self.cond.execute(executor)
		executor.stackSpace[-1].append({})
		if condition:
			self.ss1.execute(executor)
		elif hasattr(self, 'ss2'):
			self.ss2.execute(executor)
		self.subFromGCIf(executor)
		executor.stackSpace[-1].pop()
	
	def subFromGCIf(self,executor) -> None:
		curSpace = executor.stackSpace[-1][-1]
		for i in curSpace.keys():
			if(executor.getStackOrStatic(i).type== Core.REF):
				executor.gc.subtractFromGC(i)
				executor.gc.checkZero(i)