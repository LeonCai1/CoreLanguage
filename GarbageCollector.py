
class GarbageCollector:
    def __init__(self, executor) -> None:
        self.gc = []
        self.executor = executor
    def allocateGC(self) -> None:
        self.gc.append(1) #new ref variables has initial count 1.
        print(f"gc:{self.count()}")
    def addToGC(self,id) -> None:
        ref = self.executor.getStackOrStatic(id)
        if(ref.value != None):
                temp =self.gc[ref.value]
                self.gc[ref.value] = temp+1

    def subtractFromGC(self, id) -> None:
        ref = self.executor.getStackOrStatic(id)
        if(ref.value != None):
                temp =self.gc[ref.value]
                self.gc[ref.value] = temp-1

    def checkZero(self,id)-> None:
        ref = self.executor.getStackOrStatic(id)
        if ref.value != None:

            if(self.gc[ref.value] == 0):
                print(f"gc:{self.count()}")
               
   
    def count(self) -> int:
        counter =0
        for i in self.gc:
            if(i > 0):
                counter+=1
        return counter
    