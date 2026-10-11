class Person:
    name: str
    job: str
    age:str
    def __init__(self, name: str, job: str, age: str):
        self.name = name
        self.job = job
        self.age = age
person1 = Person("Anuj", "Software Engineer", "20")
person2 = Person("Jennifer", "Software Engineer", "34")
person3 = Person("alexa", "Software Engineer", "45")

print(id(person1)) # 140706982345456
print(id(person2)) # 140706982345456
print(person3) # <__main__.Person object at 0x7f8c8c8c8c8c> # This is the memory address of the object
print(person3 == person2) # False # This is because the two objects are different instances in memory


# here we can use dataclasses to make our code more readable and maintainable.
#  Dataclasses automatically generate special methods like __init__(), __repr__(), __eq__(),
# and __hash__() for us, based on the class attributes we define.

from dataclasses import dataclass,field
from time import time
import timeit
# field() function is used to customize the behavior of a dataclass field.

@dataclass(order=True,frozen=True)
# frozen=True parameter in the @dataclass decorator is used to make the class immutable,
# meaning that once an instance of the class is created, its attributes cannot be modified.


# The order=True parameter in the @dataclass decorator is used to automatically generate comparison methods
# for the class, such as __lt__(), __le__(), __gt__(), and __ge__().

#  by using the @dataclass decorator, we can define a class with attributes and the dataclass will
# automatically generate the __init__(), __repr__(), __eq__(), and __hash__() methods for us.
class Person:
    sort_index: int = field(init=False, repr=False)

    name: str
    job: str
    age: str
    strength: int = 100
    # its important to note that the order of the attributes
    # in the class definition matters when using dataclasses.



# if we want to sort person by their age we use sort_index
    def __post__init__(self):
        # self.sort_index = int(self.age)
        object.__setattr__(self, 'sort_index', int(self.age)) # This is used to set the value of sort_index attribute after the object is created.
    # The __post_init__() method is a special method that is called automatically
    # after the __init__() method of a dataclass.

person1 = Person("Anuj", "Software Engineer", "20")
person2 = Person("Jennifer", "Software Engineer", "34")
print(person1) # Person(name='Anuj', job='Software Engineer', age='20')
print(person2) # Person(name='Jennifer', job='Software Engineer', age='34')

print(person1>person2) # True # This is because the two objects are different instances in memory

print(person1) # Person(name='Anuj', job='Software Engineer', age='20', strength=100) after adding strength attribute


# after using frozen we can't be modify the age or anything
# person2.age = 20 this gives an error


#  __________________________SLOTS_________________________________

# it helps to reduce memory usage and improve performance by preventing the creation of a __dict__ for each instance of the class.
# Instead, it creates a fixed set of attributes for the class, which can be accessed
# more efficiently. This can be especially useful for classes that are expected to have a large number of instances,
# as it can help to reduce memory overhead and improve performance.
# optimize the code

# by using pip3 instal memory_profiler we can check the memory usage of our code and optimize it.
import statistics
from memory_profiler import memory_usage

class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# withouting using slots we can create a lot of objects and check the memory usage
p = PointWithoutSlots(1, 2)
print(p.__dict__) # {'x': 1, 'y': 2} # This is the memory address of the object

def create_points():
    return [PointWithoutSlots(i, i) for i in range(1000000)]

mem_values = []
time_values = []

for _ in range(10):
    mem_usage_without_slots = memory_usage(create_points,interval = 0.01)
    mem_values.append(max(mem_usage_without_slots))

    points = PointWithoutSlots(1, 2)
    time_without_slots = timeit.timeit(lambda: (points.x,points.y), number=1000000)
    time_values.append(time_without_slots)

print(statistics.mean(mem_values)) #  257.0
print(statistics.mean(time_values)) # 0.08765434567891



# ___________________WITH SLOTS __________________________
class PointWithSlots:

    __slots__ = ['x', 'y'] # This is used to define the attributes of the class and prevent the creation of a __dict__ for each instance of the class.
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = PointWithSlots(1, 2)
print(p.__dict__) # AttributeError: 'PointWithSlots' object has no attribute '__dict__' # This is because we
# have defined __slots__ in the class and it prevents the creation of a __dict__ for each instance of the class.



# withouting using slots we can create a lot of objects and check the memory usage
# p = PointWithoutSlots(1, 2)
# print(p.__dict__) # {'x': 1, 'y': 2} # This is the memory address of the object

def create_points():
    return [PointWithSlots(i, i) for i in range(1000000)]

# mem_values = []
# time_values = []

for _ in range(10):
    mem_usage_without_slots = memory_usage(create_points,interval = 0.01)
    mem_values.append(max(mem_usage_without_slots))

    points = PointWithSlots(1, 2)
    time_without_slots = timeit.timeit(lambda: (points.x,points.y), number=1000000)
    time_values.append(time_without_slots)

print(statistics.mean(mem_values)) #  123.3087654345678
print(statistics.mean(time_values)) # 0.0345678998765