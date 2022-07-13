from Core import Core
from Cond import Cond
import StmtSeq

class Loop:
	
	def parse(self, parser):
		parser.scanner.nextToken()
		self.cond = Cond()
		self.cond.parse(parser)
		parser.expectedToken(Core.BEGIN)
		parser.scanner.nextToken()
		self.ss = StmtSeq.StmtSeq()
		self.ss.parse(parser)
		parser.expectedToken(Core.ENDWHILE)
		parser.scanner.nextToken()
	
	def semantic(self, parser):
		self.cond.semantic(parser)
		parser.scopes[-1].append({})
		self.ss.semantic(parser)
		parser.scopes[-1].pop()
	
	def print(self, indent):
		for x in range(indent):
			print("  ", end='')
		print("while ", end='')
		self.cond.print()
		print(" begin\n", end='')
		self.ss.print(indent+1)
		for x in range(indent):
			print("  ", end='')
		print("endwhile\n", end='')

	def execute(self, executor):
		while self.cond.execute(executor):
			executor.stackSpace[-1].append({})
			self.ss.execute(executor)
			self.subFromGCLoop(executor)
			executor.stackSpace[-1].pop()

	def subFromGCLoop(self,executor) -> None:
		curSpace = executor.stackSpace[-1][-1]
		for i in curSpace.keys():
			if(executor.getStackOrStatic(i).type== Core.REF):
				executor.gc.subtractFromGC(i)	
				executor.gc.checkZero(i)