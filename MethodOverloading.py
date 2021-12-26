class Cls():
	def foo(self, num:int):
		print(f"Number : {num}")
		
	def foo(self, String:str):
		print(f"String : {String}")
		
	def foo(self, Lst:list):
		print(f"List : {Lst}")
		
from functools import singledispatch
class ClsWithSingleDispatch():
	@singledispatch
	def foo(self, num:int):
		print(f"Number : {num}")
		
	@foo.register(str)
	def _(self, String:str):
		print(f"String : {String}")
		
	@foo.register(list)
	def _(self, Lst:list):
		print(f"List : {Lst}")
		

if __name__ == "__main__":
	csd = ClsWithSingleDispatch()
	csd.foo(2)
	csd.foo("Two")
	csd.foo([2, "Two"])
	
	c = Cls()
	c.foo(2)
	c.foo("Two")
	c.foo([2, "Two"])