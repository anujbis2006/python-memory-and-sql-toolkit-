# first  class function in python
# * they are instance of some class called function
# * can be stored in data structures, can be passed as arguments to other functions, and can be returned from functions as well.
#  * can be sassigned to variables.
# * can perform operations on these objects .
#  * can be passsed as arguments to functions .

# 1 .
print(type('hello')) # <class 'str'>

# 2.
str1 = 'Hello'
print(str1) # hello

# 3.
names = ['Anuj', 'Arjun', 'Amit']
# can be stored in a data structure like list
print(names) # ['Anuj', 'Arjun', 'Amit']

# 4.
def greet(name):
    return f"Hello, {name}!"
greeting = greet('Anuj') # can be assigned to a variable
print(greeting) # Hello, Anuj!
# we can pass an argument to a function and return a value from it.

# 5.
def greet(name):
    return f"Hello, {name}!"
greeting = greet()
print(greeting) # Hello, Anuj!
# we can pass the function as an argument to another function and return a value from it.

# 6.
def greet(name):
    print(name)

data = [greet]
print(data) # [<function greet at 0x7f8c8c8c8c8c>]
# we can also store the function in a data structure like list and return a value from it.

# 7.
def display(msg):
    print(msg)

def demo(func):
    pass
demo(display) # we can also pass the function as an argument to another function and return a value from it.

# 8.
# 7.
def display(msg):
    def xyz():
        pass
    print(msg)

def demo(func):
    pass
demo(display) 
# so here 