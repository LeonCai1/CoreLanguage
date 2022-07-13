Name: Leon Cai
file:
**
New files:
GabageCollector.py: The GabageCollector initialize a heap for gc and have several methods for gc.
	allocateGC: allocate the gc whenever heap is allocated.
	addToGC: add the ref variable's count to the gc
	subtractFromGC: subtract the count of ref varaible in gc
	checkZero: check if the current count for a ref variable is 0. It true, print the current total count for gc
	count: count total live ref variables.
**

-------------------Overall design-------------------------------
For this lab is basically implement the gc. The way I think is 
whenever the heap is changed, GC needed to have a corresponding way
to change the value in it. Another import thing is handling gabadge
before the local scope is popped out.
----------------------------------------------------------------

Changes:
In Program.py, if.py, loop.py add subFromGC methods to handle gabage collection before the local fram is pop out.
In Executor, make a GC object.