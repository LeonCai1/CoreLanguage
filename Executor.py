from Scanner import Scanner
from Core import Core
import sys
from GarbageCollector import GarbageCollector

class CoreVar:
    def __init__(self, varType):
        self.type = varType
        self.value = None

        if self.type == Core.INT:
            self.value = 0

class Executor:

    def __init__(self, s):
        self.globalSpace = {}
        self.stackSpace = [] # stack of frames(stacks)
        self.heapSpace = []
        self.functionMap = {}
        self.dataFile = Scanner(s)
        self.gc = GarbageCollector(self)
    def pushLocalScope(self):
        self.stackSpace.append([])
        self.stackSpace[-1].append({})
        
    def popLocalScope(self):
        self.stackSpace.pop()

    
    def getNextData(self):
        data = 0
        if self.dataFile.currentToken() == Core.EOS:
            print("ERROR: data file is out of values!\n", end='')
            sys.exit()
        else:
            data = self.dataFile.getCONST()
            self.dataFile.nextToken()
        return data
	
    def allocate(self, identifier, varType):
        record = CoreVar(varType)
        # If we are in the DeclSeq, the local scope will not be created yet
        if len(self.stackSpace)==0:
            self.globalSpace[identifier] = record
        else:
            self.stackSpace[-1][-1][identifier] = record

	
    def getStackOrStatic(self, identifier):
        record = None

        for x in reversed(self.stackSpace[-1]):
            if identifier in x:
                record = x[identifier]
                break
        if record == None:
            record = self.globalSpace[identifier]
        return record
	
    def heapAllocate(self, identifier):
        x = self.getStackOrStatic(identifier)
        if x.type != Core.REF:
            print("ERROR: " + identifier + " is not of type ref, cannot perform \"new\:-assign!\n", end='')
            sys.exit()
        x.value = len(self.heapSpace)
        self.heapSpace.append(None)
        
        # print("gc:"+self.gc.count())
	
    def getType(self, identifier):
        x = self.getStackOrStatic(identifier)
        return x.type
	
    def getValue(self, identifier):
        x = self.getStackOrStatic(identifier)
        value = x.value
        if x.type == Core.REF:
            try:
                value = self.heapSpace[value]
            except IndexError:
                print("ERROR: invalid heap read attempted!\n", end='')
                sys.exit()
            except TypeError:
                print("ERROR: invalid heap read attempted!\n", end='')
                sys.exit()
        return value
	
    def storeValue(self, identifier, value):
        x = self.getStackOrStatic(identifier)
        if x.type == Core.REF:
            try:
                self.heapSpace[x.value] = value
                # temp =self.gc[x.value]
                # self.gc[x.value] = temp+1
            except IndexError:
                print("ERROR: invalid heap write attempted!\n", end='')
                sys.exit()
            except TypeError:
                print("ERROR: invalid heap write attempted!\n", end='')
                sys.exit()
        else:
            x.value = value

    def referenceCopy(self, var1, var2):
        x = self.getStackOrStatic(var1)
        y = self.getStackOrStatic(var2)
        self.gc.addToGC(var2)
        self.gc.subtractFromGC(var1)	
        self.gc.checkZero(var1)
        x.value = y.value


