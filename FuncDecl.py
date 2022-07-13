from Core import Core
from Id import Id
from StmtSeq import StmtSeq
from Formals import Formals
import sys
class FuncDecl:
    def parse(self, parser):
        self.id = Id()
        self.id.parse(parser)
        # check (
        parser.expectedToken(Core.LPAREN)
        parser.scanner.nextToken()
 
        #check ref keyword
        parser.expectedToken(Core.REF)
        parser.scanner.nextToken()
        #call formal class
        self.f = Formals()
        self.f.parse(parser)
        #check )
        parser.expectedToken(Core.RPAREN)
        parser.scanner.nextToken()
        #check begin keyword
        parser.expectedToken(Core.BEGIN)
        parser.scanner.nextToken()

        # call statement sequence class
        self.ss = StmtSeq()
        self.ss.parse(parser)
        #check endfunc
        parser.expectedToken(Core.ENDFUNC)
        parser.scanner.nextToken()
    def semantic(self,parser):
        # check function name duplication
        if self.id.getString() in parser.functionMap:
            print(f"ERROR: Function{self.id.getString()} has been declared.")
            sys.exit()
        #put the function name in scope
        parser.functionMap[self.id.getString()] = self

    
    def print(self, indent):
        for x in range(indent):
            print("  ", end='')
        self.id.print()
        print('(ref ', end='')
        self.f.print(indent)
        print(') begin\n', end='')
        self.ss.print(indent +1)
        for x in range(indent):
            print("  ", end='')       
        print('endfunc\n', end='')
    
    #Todo: execute method
    def execute(self,executor):
        executor.functionMap[self.id.getString()] = self
