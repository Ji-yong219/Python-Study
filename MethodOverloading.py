class Cls():
	def foo(self):
		print("Nothing")
		
	def foo(self, num):
		print(f"Number : {num}")
		
	def foo(self, num, String):
		print(f"Number : {num}\tString : {String}")
		
	def foo(self, num, String, Lst):
		print(f"Number : {num}\tString : {String}\tList : {Lst}")
		
from functools import singledispatch
import numbers
class ClsWithSingleDispatch():
	@singledispatch
	def foo(self):
		print("Nothing")
		
	@foo.register(int)
	def _(self, num:int):
		print(f"Number : {num}")
		
	@foo.register(int)
	@foo.register(str)
	def _(self, num:int, String:str):
		print(f"Number : {num}\tString : {String}")
		
	@foo.register(int)
	@foo.register(str)
	@foo.register(list)
	def _(self, num:int, String:str, Lst:list):
		print(f"Number : {num}\tString : {String}\tList : {Lst}")
		

if __name__ == "__main__":
	csd = ClsWithSingleDispatch()
	csd.foo()
	csd.foo(2)
	csd.foo(2, "Two")
	csd.foo(2, "Two", [2, "Two"])
	
	c = Cls()
	c.foo()
	c.foo(2)
	c.foo(2, "Two")
	c.foo(2, "Two", [2, "Two"])