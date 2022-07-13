from Decl import Decl
from Core import Core
from FuncDecl import FuncDecl

class DeclSeq:
	
	def parse(self, parser):
		#check if it is <decl> or <func_decl>
		if parser.scanner.currentToken() == Core.INT or parser.scanner.currentToken() == Core.REF:
			self.decl = Decl()
			self.decl.parse(parser)
		elif parser.scanner.currentToken() == Core.ID:
			self.fd = FuncDecl()
			self.fd.parse(parser)

		if parser.scanner.currentToken() != Core.BEGIN:
			self.ds = DeclSeq()
			self.ds.parse(parser)

	def semantic(self, parser):
		if hasattr(self,'decl'):
			self.decl.semantic(parser)
		else:
			self.fd.semantic(parser)
		if hasattr(self, 'ds'):
			self.ds.semantic(parser)
	
	def print(self, indent):
		if hasattr(self,'decl'):
			self.decl.print(indent)
		else:
			self.fd.print(indent)
		if hasattr(self, 'ds'):
			self.ds.print(indent)

	def execute(self, executor):
		if hasattr(self, 'decl'):
			self.decl.execute(executor)
		else:
			self.fd.execute(executor)
		if hasattr(self, 'ds'):
			self.ds.execute(executor)