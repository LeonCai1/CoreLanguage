from Id import Id
from Core import Core

class Formals:
    
    def parse(self, parser):
        self.id= Id()
        self.id.parse(parser)
        if parser.scanner.currentToken() == Core.COMMA:
            parser.scanner.nextToken()
            self.f = Formals()
            self.f.parse(parser)
    
    def semantic(self,parser):
        self.id.doublyDeclared(parser)
        self.id.addToScopes(parser, Core.REF)
        if hasattr(self,'f'):
            self.f.semantic(parser)

    def print(self, indent):
        self.id.print()
        if hasattr(self, 'f'):
            print(', ', end='')
            self.f.print(indent)
        
    #return param list 
    def getParam(self):

        if hasattr(self, 'f'):
            paramList = self.f.getParam()
        else:
            paramList = []
        paramList.append(self.id.getString())
        return paramList
        

