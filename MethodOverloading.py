class Cls():
	def do(self):
		print("Nothing")
		
	def do(self, num):
		print(f"Number : {num}")
		
	def do(self, num, String):
		print(f"Number : {num}\tString : {String}")
		
	def do(self, num, String, Lst):
		print(f"Number : {num}\tString : {String}\tList : {Lst}")
		
from functools import singledispatch
import numbers
class ClsWithSingleDispatch():
	@singledispatch
	def do(self):
		print("Nothing")
		
	@do.register(int)
	def _(self, num:int):
		print(f"Number : {num}")
		
	@do.register(int)
	@do.register(str)
	def _(self, num:int, String:str):
		print(f"Number : {num}\tString : {String}")
		
	@do.register(int)
	@do.register(str)
	@do.register(list)
	def _(self, num:int, String:str, Lst:list):
		print(f"Number : {num}\tString : {String}\tList : {Lst}")
		

if __name__ == "__main__":
	csd = ClsWithSingleDispatch()
	csd.do()
	csd.do(2)
	csd.do(2, "Two")
	csd.do(2, "Two", [2, "Two"])
	
	c = Cls()
	c.do()
	c.do(2)
	c.do(2, "Two")
	c.do(2, "Two", [2, "Two"])