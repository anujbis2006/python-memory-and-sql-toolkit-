def outer_function():
    message = 'Hi'
    def inner_function():
        print(message)
    return inner_function

my_func = outer_function()  # This will print 'Hi' because inner_function has access to the message variable in the outer_function's scope
my_func()  # Output: Hi


# Decorator - A decorator is a function that takes another function as an argument,
#  adds some functionality to it, and returns a new function.
# Decorators are often used to modify the behavior of functions or methods.

def decorator_function(original_function):
    def wrapper_function():
        print('Wrapper function executed this befor e {}'.format(original_function.__name__))
        # here we can add some functionality before calling the original function
        return original_function()
    return wrapper_function

def display():
    print('Display function ran')

decorated_display = decorator_function(display)
decorated_display()  # Output: Display function ran

# So in this example , the decorator_function takes the display function as an argument,
# and returns a new function (wrapper_function) that calls the original display function.
# When we call decorated_display(), it runs the wrapper_function,
# which in turn calls the original display function.

# why we use that -  Because decorators allow us to easily add functionality to existing functions without modifying their code.



def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print('Wrapper function executed this befor e {}'.format(original_function.__name__))
        # here we can add some functionality before calling the original function
        return original_function(*args, **kwargs)
    return wrapper_function

@decorator_function
def display():
    print('Display function ran')

display()  # Output: Display function ran

# So here we use the @decorator_function syntax to apply the decorator to the display function.
# this works same as decorated_display = decorator_function(display) and then calling decorated_display().

@decorator_function
def display_info(name,age):
    print('Display function ran with arguments ({}, {})'.format(name, age))

# If we use the @dectorator_function it will give the error which is because
# the wrapper_function does not accept any arguments beacuse in wrapper funciton it takes 0 arguments
# but in display_info it pass 2 argument
# , but the display_info function does.

# so the solution is to use *args and **kwargs in the wrapper_function to accept any
#  number of positional and keyword arguments,

display_info('Anuj', 20)  # Output: Display function ran with arguments (Anuj, 20)
display() # Output: Display function ran

class decorator_class(object):
    def __init__(self,original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print('wrapper class executed this before {}'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)



@decorator_class
def display():
    print('Display function ran')

display()

@decorator_class
def display_info(name,age):
    print('Display function ran with arguments ({}, {})'.format(name, age))

display_info('Anuj', 20)
display() # Output: Display function ran

#  so its same as the decorator_function but here we use class instead of
# function and we use __call__ method to make the class callable.

def my_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)

    def wrapper(*args,**kwargs):
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_func(*args, **kwargs)
    return wrapper

# so here we use the logging module to log the arguments and
# keyword arguments passed to the original function.
# and inside it the wrapper function we log the arguments and
#  keyword arguments passed to the original function and then call the original function.
# and in last we return the wrapper function which is returned by the my_logger fucntion.
# that work which is done inside the it ..

def my_timer(orig_func):
    import time
    def wrapper(*args,**kwargs):
        t1 = time.time()
        result = orig_func(*args,**kwargs)
        t2 = time.time()-t1
        print('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result
    return wrapper

# so here we use the time module to measure the time taken by the original function to run.
# and inside it the wrapper function we measure the time taken by the original function to run and then call the original function.
# t1 = time.time() # this will give the current time in seconds since the epoch.
# result = orig_func(*args,**kwargs) # this will call the original function and pass the arguments and keyword arguments to it.
# t2 = time.time()-t1 # this will give the time taken by the original
# and in last we return the result of the original function which is returned by the wrapper function.


@my_logger
def display_info(name,age):
    print('Display_info ran with arguments ({}, {})'.format(name, age))

display_info('Anuj', 20)  # Output: Display_info ran with arguments (Anuj, 20)


from ast import arg
import time

@my_timer
def display_info(name,age):
    time.sleep(1)
    print('Display_info ran with arguments ({}, {})'.format(name, age))

# now we can use both the decorators together to log the arguments and keyword arguments passed to the original function and
# also measure the time taken by the original function to run.

@my_timer
@my_logger
def display_info(name,age):
    time.sleep(1)
    print('Display_info ran with arguments ({}, {})'.format(name, age))

display_info('Anuj', 20)  # Output: Display_info ran with arguments (Anuj, 20)
                                    #  wrapper ran in : 1.001 sec
#  get some unexpected output because the order of the decorators matters.


@my_logger
@my_timer
def display_info(name,age):
    time.sleep(1)
    print('Display_info ran with arguments ({}, {})'.format(name, age))

display_info = my_logger(my_timer(display_info))  # Output: Display_info ran with arguments (Anuj, 20)
# so all of that we do here is equal "my_timer(display_info) " to wrapper funtion
display_info('Anuj', 20)  # Output: Display_info ran with arguments (Anuj, 20)
print(display_info.__name__)  # Output:wrapper

from functools import wraps
def my_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args,**kwargs):
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs))
        return orig_func(*args, **kwargs)
    return wrapper



def my_timer(orig_func):
    import time
    @wraps(orig_func)
    def wrapper(*args,**kwargs):
        t1 = time.time()
        result = orig_func(*args,**kwargs)
        t2 = time.time()-t1
        print('{} ran in: {} sec'.format(orig_func.__name__, t2))
        return result
    return wrapper

def display_info(name,age):
    time.sleep(1)
    print('Display_info ran with arguments ({}, {})'.format(name, age))

display_info = my_timer(display_info)
print(display_info.__name__)  # Output:disply_info
display_info('Anuj', 20)  # Output: Display_info ran with arguments (Anuj, 20)



@my_logger
@my_timer

def display_info(name,age):
    time.sleep(1)
    print('Display_info ran with arguments ({}, {})'.format(name, age))
display_info('Anuj', 20)
# so here we use the @wraps decorator from the functools module to preserve the original function's metadata (like its name and docstring) when we wrap it with our decorator.
# a nf we didn;t have to wirte manually for another fucntion of my logger and my timer we can use the @wraps decorator to preserve the original function's metadata
# (like its name and docstring) when we wrap it with our decorator.


# 1.Problem 1 timing function execution time
import time
def timer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        result  = func(*args,**kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to execute.")
        return result
    return wrapper

@timer
def log_time(n):
    time.sleep(n)
    print(f"Function executed after {n} seconds.")
# output - fucntion log_time took 2.002 seconds to execute.

# 2. Debugging Fucntions Calls

def debug(func):
    def wrapper(*args,**kwrags):
        args_value = ', '.join(str(arg) for arg in args)
        kwargs_value = ', '.join(f"{k}={v}" for k,v in kwrags.items())
        print(f"Calling {func.__name__} with arguments: {args_value} and keyword arguments: {kwargs_value}")
        return func(*args,**kwrags)
        return wrapper
@debug
def greet(name , greeting = "Hello"):
    print(f"{greeting}, {name}!")

    # 3. cach return values of a function
    import time
def cache(func):
    cached_results = {}
    def wrapper(*args):
        if args in cached_results:
            return cached_results[args]

        result = func(*args)
        cached_results[args] = result
        return result
    return wrapper



def long_running_function(a,b):
    time.sleep(4)
    return a+b


long_running_function = cache(2,3)
long_running_function(2,3)  # This will take 4 seconds to execute and return 5