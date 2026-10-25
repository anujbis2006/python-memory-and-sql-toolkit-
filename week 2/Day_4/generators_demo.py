# iterator and iterable are two different concepts in Python.
# An iterable is an object that can be iterated over, meaning that it can be used in a for loop or in any other context that requires iteration.
# An iterator is an object that represents a stream of data and can be used to iterate over the elements of an iterable.
# Examples of iterables include lists, tuples, sets, and dictionaries.

# Examples of iterators include the objects returned by the iter() function, which can be used to iterate over the elements of an iterable.
from itertools import count


nums = [1, 2, 3, 4, 5]
it = iter(nums)  # Create an iterator from the list
print(next(it))  # Output: 1
print(next(it))  # Output: 2
print(next(it))  # Output: 3

# examlpe of iterable
for num in nums:
    print(num)  # Output: 1, 2, 3, 4, 5


# Generators are a special type of iterator that allow you to create an iterator in a more concise way.
# They are defined using a function that contains one or more yield statements.
def my_generator():
    yield 1
    yield 2
    yield 3

# yield is a keyword that is used to produce a value from the generator function and pause its execution, allowing it to be resumed later.
# generators are not hold the entire sequence in memory, but instead generate the values on-the-fly as they are requested.
# This makes them more memory-efficient than lists or other data structures that hold all the values in memory at once.
g = my_generator() # Create a generator object
print(next(g))  # Output: 1
print(next(g))  # Output: 2
print(next(g))  # Output: 3

import mem_profile
import random
import time

names = ['John', 'Corey', 'Adam', 'Steve', 'Rick', 'Thomas']
majors = ['Math', 'Engineering', 'CompSci', 'Arts', 'Business']

print ('Memory (Before): {}Mb'.format(mem_profile.memory_usage_psutil()))

def people_list(num_people):
    result = []
    for i in range(num_people):
        person = {
                    'id': i,
                    'name': random.choice(names),
                    'major': random.choice(majors)
                }
        result.append(person)
    return result

def people_generator(num_people):
    for i in range(num_people):
        person = {
                    'id': i,
                    'name': random.choice(names),
                    'major': random.choice(majors)
                }
        yield person

t1 = time.clock()
people = people_list(1000000)
t2 = time.clock()
# before caaling base memory = 15.2345
# after calling base memory =  150.2345
#


t1 = time.clock()
people = people_generator(1000000)
t2 = time.clock()
# before caaling base memory = 15.2345
# after calling base memory =  15.2345 beacuse it doesnt hold the rnitre the sequence in memory, but instead generates the values on-the-fly as they are requested.
#  but if we created a list then it will hold the entire sequence in memory, and it will take more memory.and give the same output as the list. but if we created a list then it will hold the entire sequence in memory, and it will take more memory.



print ('Memory (After) : {}Mb'.format(mem_profile.memory_usage_psutil()))
print ('Took {} Seconds'.format(t2-t1))



# what happens when a for loop runs? (60 seconds)
#  when loops run, they create an iterator object that keeps track of the current position in the sequence.
# and like an example if we have a list of 10 elements, the for loop will create an iterator object that
# will keep track of the current position in the list , the loops iterates over the element of the list until it reaches to the false value,
# and then it will stop iterating. and the iterator object will be destroyed after the loop is finished.


# send() and close()
# They are two additional methods that can be used with generators to control their behavior.
# The send() method allows you to send a value to the generator function, which can be
    # used to modify its behavior or provide additional input. The close() method allows 
    # you to terminate the generator function and free up any resources it may be using.

# The close() method is used to terminate a generator function and free up any resources it 
# may be using. When a generator function is closed, it raises a GeneratorExit exception, which 
# can be caught by the generator function to perform any necessary cleanup before exiting.

# Example - 

# For send() method, we can use it to send a value to the generator function, 
# which can be used to modify its behavior or provide additional input. 
# The generator function can receive the value sent by the send() method and use 
# it to produce a new value or modify its internal state.
def my_generator():
    x = yield "Ready"
    print("Received:", x)

    yield "Finished"


g = my_generator()

print(next(g))       # Ready
print(g.send(100))   # Received: 100, then Finished


# for close() method , we can use it to terminate a generator
#  function and free up any resources it may be using. 
# When a generator function is closed, it raises a GeneratorExit 
# exception, which can be caught by the generator function to 
# perform any necessary cleanup before exiting.


def my_generator():
    try:
        yield "First item"
        yield "Second item"
        yield "Third item"
    finally:
        print("Generator stopped and cleanup executed")


g = my_generator()

print(next(g))
g.close()
print("Program continues")

# OutPut:

# First item
# Generator stopped and cleanup executed
# Program continues


