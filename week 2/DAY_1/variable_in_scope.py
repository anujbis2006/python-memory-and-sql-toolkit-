# local scope
def func():
    a = 10
    print(a)

func()
# print(a) # This will raise a NameError because 'a' is not defined in the global scope.

# global scope
b = 20
def func():
    print(b)

func()
print(b)  # This will print 20 because 'b' is defined in the global scope.

# if both gloval and local variable are same.
a = 30  # global variable
def func():
    a = 40  # local variable
    print(a)  # This will print 40 because the local variable 'a' shadows the global variable 'a'.
func() # this will print 40 because the local variable 'a' shadows the global variable 'a'.
print(a)  # This will print 30 because the global variable 'a' is still

# global keyword
a = 50  # global variable
def func():
    global a  # This tells Python that we want to use the global variable 'a'
    a = 60  # This modifies the global variable 'a'
    print(a)  # This will print 60 because we modified the global variable 'a'.
func() # this will print 60 because we modified the global variable 'a'.
print(a)  # This will print 60 because the global variable 'a' was modified


# non local keyword
def outer_func():
    a = 70  # This is a variable in the enclosing scope

    def inner_func():
        nonlocal a  # This tells Python that we want to use the variable 'a' from the enclosing scope
        a = 80  # This modifies the variable 'a' in the enclosing scope
        print(a)  # This will print 80 because we modified the variable 'a' in the enclosing scope

    inner_func()  # Call the inner function
    print(a)  # This will print 80 because the variable 'a' in the enclosing scope was modified

# enclosed scope
def outer_func():
    a = 70  # This is a variable in the enclosing scope

    def inner_func():
        print(a)  # This will print 70 because 'a' is in the enclosing scope of 'inner_func'

    inner_func()  # Call the inner function

# inbuilt scope
# Python has a built-in scope that contains all the built-in functions and variables.
def func():
    print(len)  # This will print the built-in 'len' function
    