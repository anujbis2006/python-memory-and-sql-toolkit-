# #🔴Early Binding (Static Binding) (Compile Time Binding)

# Binding means mapping of one thing to another.
# The link between a function call and function definition.
# Whenever we call a function, the program control binds the
# memory address where the function is defined. 
# Function call and function definition are linked at compile time.
# All the information needed to call the function is available during compile time.
# Everything needed is available during compile time therefore, this is generally faster than runtime binding.
# No Polymorphic behavior 
# 
# Examples: function overloading and operator overloading
# Function overloading video
# 
# 🔴Late Binding (Dynamic Binding) (Runtime Binding)

# The function call and function definition aren’t linked until runtime.
# Information can’t be determined until runtime.
# Slower than early binding.
# Adopts Polymorphism
# Examples: Dynamic Binding can be achieved through virtual functions.
# 
# 
# late binding
# late binding is a programming concept that refers to the process of 
# determining the method or function to be called at runtime, 
# rather than at compile time. In other words, it allows for dynamic method 
# resolution based on the actual type of the object being referenced, rather than the 
# type of the reference itself. This is in contrast to early binding, where the method or function to be called is determined 
# at compile time based on the static type of the reference.

func = []
for i in range(3):
    func.append(lambda: i)

for f in func:
    print(f())  # Output: 2, 2, 2

# Late binding in Python means that variables used inside closures or nested functions are looked up at the time the function is called, rather than when it is defined

# ❌ The Classic Pitfall: Functions in a Loop


# Intention: Create a list of functions that multiply by 0, 1, 2, and 3
multipliers = [lambda x: i * x for i in range(4)]

# Let's call them expecting: 0*10, 1*10, 2*10, 3*10
results = [func(10) for func in multipliers]
print(results) 

# Expected Output:
# [0, 10, 20, 30]
# Actual Output:
# [30, 30, 30, 30]
# Why this happens:
# The generated lambda functions do not store their own separate copies of i. They all share a reference to the exact same outer variable i. By the time you actually execute func(10), the loop has already completed, and the value of i is left sitting at its final iteration value: 3. Consequently, every single function calculates 3 * 10


# How to Fix It (Enforcing Early Binding)
# To fix this, you must force Python to evaluate and lock in the value of the variable at the exact moment the function is created. There are three standard workarounds:
# 1. Using Default Arguments (Most Common & Pythonic)
# Python evaluates default arguments once—exactly at the time of function definition. By binding i as a default parameter, you capture its value on every loop step.
# python
multipliers = [lambda x, i=i: i * x for i in range(4)]
results = [func(10) for func in multipliers]
print(results)  # Output: [0, 10, 20, 30]
# Use code with caution.

# 2. Using functools.partial

# The partial function allows you to pre-bind arguments to a callable object immediately upon creation.
# python
# from functools import partial

def multiply(x, i):
    return i * x

# partial instantly binds the current value of i to each new function
multipliers = [partial(multiply, i=i) for i in range(4)]

results = [func(10) for func in multipliers]
print(results)  # Output: [0, 10, 20, 30]
# Use code with caution.

# 3. Using a Factory Function

# You can wrap the creation in an outer helper function. Because arguments inside functions belong to a distinct local scope, passing the variable isolates its current value.
# python
def make_multiplier(i):
    return lambda x: i * x

multipliers = [make_multiplier(i) for i in range(4)]

results = [func(10) for func in multipliers]
print(results)  # Output: [0, 10, 20, 30]
# Use code with caution.

# 💡 The Silver Lining: Why Late Binding Exists

# While late binding can be a tricky "gotcha" in loops, it is actually a core feature that gives Python its runtime flexibility. It allows for features like:
# • Dynamic updates: If a global or outer variable changes, any functions relying on it will automatically use the updated value without needing definition updates.
# • Duck Typing & Polymorphism: Objects can resolve their methods and properties at runtime based on the actual object instance being processed, facilitating dynamic code evaluation.
# If you are trying to debug a specific block of code experiencing this behavior, feel free to paste your code here, or tell me what kind of loop structure you are using so we can fix it!
