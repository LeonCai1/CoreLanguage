from Id import Id
from Core import Core
from Formals import Formals
import StmtSeq
import sys

class FuncCall:
    countRef = 0
    def parse(self, parser):
        # check begin keyword
        parser.expectedToken(Core.BEGIN)
        parser.scanner.nextToken()
        # call Id class
        self.id = Id()
        self.id.parse(parser)
        # check (
        parser.expectedToken(Core.LPAREN)
        parser.scanner.nextToken()
        # call formal class
        self.f = Formals()
        self.f.parse(parser)
        # check )
        parser.expectedToken(Core.RPAREN)
        parser.scanner.nextToken()       
        #check ;
        parser.expectedToken(Core.SEMICOLON)
        parser.scanner.nextToken() 

    def semantic(self, parser):
        #check whether the function has been declared or not:
        if not self.id.getString() in parser.functionMap:
            print("ERROR: Cannot call a function which is not declared yet")
            sys.exit()
        callee = parser.functionMap[self.id.getString()]
        #get param list
        actualParamList = self.f.getParam()
        formalParamList = callee.f.getParam()
        #check if the num of param is right
        if not len(actualParamList) == len(formalParamList):
            print("ERROR: Parameters not match")

        #check if the parameters of the function has beed declared before using
        for x in actualParamList:
            if parser.nestedScopeCheck(x) == Core.ERROR:
                print("ERROR: Using id before declaration")
                sys.exit()
        functionScope = []
        functionScope.append({})

        for x in formalParamList:
            functionScope[-1][x] =Core.REF

        parser.scopes.append(functionScope)
        parser.scopes[-1].append({})
        self.f.semantic(parser)
        parser.scopes.pop()


    def print(self, indent):
        for x in range(indent):
            print("  ", end='')
        print('begin ', end='')
        self.id.print()
        print('(', end='')
        self.f.print(indent)
        print(');\n', end='')

    #Todo: execute method
    def execute(self,executor):
        # when function is called by caller, retrieve the body and formal param of callee
        callee = executor.functionMap[self.id.getString()]
        functionBody = callee.ss
        #get param list
        actualParamList = self.f.getParam()
        formalParamList = callee.f.getParam()
        # create function frame in stack of frame
        frame = self.createFunctionFrame(actualParamList, formalParamList,executor)

        #push the frame into stack
        executor.stackSpace.append(frame)
        #execute the frame

 
        functionBody.execute(executor)

        #clean gc for current function frame
        self.subFromGCFrame(frame, executor)
        #pop out the frame after execution
        executor.popLocalScope()

		#helper function for execute to create the frame for function.
    def createFunctionFrame(self,actualParam, formalParam,executor):
        frame = []
        for i in range(len(formalParam)):
            actualCovar = executor.getStackOrStatic(actualParam[i])
            frame.append({formalParam[i]:actualCovar }) 
            # check add new ref variables in this frame into gc heap
            if(executor.getStackOrStatic(actualParam[i]).type == Core.REF):
                executor.gc.addToGC(actualParam[i])
                
        return frame
    #before pop out the function frame, subtract ref variables declared inside the frame.    
    def subFromGCFrame(self, frame, executor) -> None:
        temp = frame
        for i in range(len(temp)):
            for id in temp[-1].keys():
                if executor.getStackOrStatic(id)!= None:
                    var = executor.getStackOrStatic(id)
                    if(var.type == Core.REF):
                        executor.gc.subtractFromGC(id)
                        executor.gc.checkZero(id)
                       
            temp.pop()
        
            
