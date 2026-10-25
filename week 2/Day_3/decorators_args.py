# Decorator factory 
# Is a function that returns a decorator, 
# allowing you to pass configuration arguments to customize 
# how the decorator behaves.

# When you hear about a "decorator factory with 3 factors," 
# it typically refers to a design pattern or structure that 
# relies on three specific architectural layers (or factors) 
# to work.

# To build a configurable decorator, your code must nesting three distinct 
# functions inside one another. Each layer has a specific "factor" or responsibility:

# 1. The Factory Layer (Configuration Arguments):
# This is the outermost function. It accepts the custom 
# configurations, settings, or flags ("factors") you want to apply. 
# It does not touch the actual code execution; it just sets the stage.

# 2. The Decorator Layer (The Target):
# This is the middle function. It automatically receives the 
# target component—such as the function, method, or class being 
# decorated.

# 3. The Wrapper Layer (The Logic & Execution):
# This is the innermost function. It intercepts 
# the arguments passed to the original function, executes 
# your custom decorator logic using the configurations from 
# Layer 1, runs the original function, and returns the result.

# Example: A Rate Limiter Decorator Factory
# Design a rate limiter 
# 3 factors in which it uses (max_calls,time_window and error message) to dynamically control functions.


import time 

def rate_limiter(mac_calls,time_window,error_message):
#   this decorator factor recives the target functions.
    def decorator(func):
        #  State tracking for rate limiter
        call_timestamps = []


        # The wrapper layer : its handles execition and logic of the target function.
        def wrapper(*args,**kwargs):
            current_time = time.time()

            # remove timestamps that are outside the time window
            #  using a list comprehension (to reassign to keep it clean)

            nonlocal call_timestamps
            call_timestamps = [timestamp for timestamp in call_timestamps if current_time - timestamp < time_window]

            # check if limit is exceeded
            if len(call_timestamps) >= mac_calls:
                raise PermissionError(error_message)

            # log this call and execute the original function
            call_timestamps.append(current_time)
            return func(*args,**kwargs)

        return wrapper
    return decorator


# where we can use this up by calling the api requests
# Applying the decorator factory with 3 custom factors:
# Factor 1: 3 max calls
# Factor 2: 10.0 seconds window
# Factor 3: "Too fast!" custom message

@rate_limiter(mac_calls = 3,time_window = 10.0,error_message = "Too fast!")
def request_api_data():
    return f"API request made" {user_id}

# ____Testing the rate limiter____
print(request_api_data("Alice"))  # Works (Call 1)
print(request_api_data("Alice"))  # Works (Call 2)
print(request_api_data("Alice"))  # Works (Call 3)

try :
    print(request_api_data("Alice"))  # Throws Error (Call 4 inside 10s)
except PermissionError as e:
    print(f"Blocked: {e}")


# Designing LRU Chache with Decorator Factory (Least Recently Used)

from collections import OrderedDict
class SimpleLRUCache:
    def __init__(self,max_size):
        self.max_size = max_size
        self.cache = OrderedDict()

    def get(self,key):
        if key not in self.cache:
            return None

        # Move the accessed item to the end to show that it was recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self,key,value):
        if key in self.cache:

            # Update the value and move it to the end to show that it was recently used
            self.cache.move_to_end(key)
        self.cache[key] = value

        # if we exceed the capacity of the cache , then remove the least recently used item
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False) # pop the first item (the least recently used one)

@SimpleLRUCache(max_size=3)
def get_data_from_db(query):
    # Simulate a database query
    time.sleep(1)  # Simulating delay
    return f"Results for {query}"
get_data_from_db("SELECT * FROM users")  # Takes time, caches result
get_data_from_db("SELECT * FROM users")  # Returns cached result, fast
