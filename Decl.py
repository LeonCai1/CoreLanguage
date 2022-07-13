from DeclInt import DeclInt
from DeclRef import DeclRef
from Core import Core

class Decl:
	
	def parse(self, parser):
		if parser.scanner.currentToken() == Core.INT:
			self.declInt = DeclInt()
			self.declInt.parse(parser)
		else:
			self.declRef = DeclRef()
			self.declRef.parse(parser)
	
	def print(self, indent):
		if hasattr(self, 'declInt'):
			self.declInt.print(indent)
		elif hasattr(self, 'declRef'):
			self.declRef.print(indent)
			
	def semantic(self, parser):
		if hasattr(self, 'declInt'):
			self.declInt.semantic(parser)
		elif hasattr(self, 'declRef'):
			self.declRef.semantic(parser)

	def execute(self, executor):
		if hasattr(self, 'declInt'):
			self.declInt.execute(executor)
		elif hasattr(self, 'declRef'):
			self.declRef.execute(executor)