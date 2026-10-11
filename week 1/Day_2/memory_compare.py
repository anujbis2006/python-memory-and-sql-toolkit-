# Dunder Methods / Magic Methods
# because they are surrounded with double underscores
# this are special methods that allow us to define how our objects behave with built-in Python operations.
# builing operators like +, -, *, /, ==, <, >, etc. are implemented using dunder methods.

# __xyz__ methods are called dunder methods because they have double underscores before and after their name.
# 1. __init__: this method is initlaiz object and the __STAR__ method
# define how the object is represented as string when we print it or convert it to a string using str() function.

class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name} is {self.age} years old"

# create an instance
Person = person('Anuj', 20)
print(Person) # Anuj is 20 years old

# 2. __add__: this method is used to define how the object behaves when we use the + operator with it.
class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __add__(self,other):
        return point(self.x + other.x, self.y + other.y)
    def __str__(self):
        return f"({self.x}, {self.y})"


    # create two points objexts
p1 = point(1,2)
p2 = point(5,5)

# adding these using + operator
p3 = p1 + p2

# display the result
print(p3) # (6, 7)

# 3. __repr__: this method is used to define how the object is represented as a string when we use the repr() function or when we print the object in the interactive shell.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __repr__(self):
        return f"person('{self.name}', {self.age})"

Person = person('Anuj', 20)
print(repr(Person)) # person('Anuj', 20)

# 4. __eq__: this method is used to define how the object behaves when we use the == operator with it.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __eq__(self,other):
        return self.name == other.name and self.age == other.age
Person1 = person('Anuj', 20)
Person2 = person('Anuj', 20)
print(Person1 == Person2) # True

# 5 __hash__: this method is used to define how the object behaves when we use the hash() function with it.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __hash__(self):
        return hash((self.name, self.age))
Person = person('Anuj', 20)
print(hash(Person)) # 1234567890 (the hash value will be different each time

# 6. __len__: this method is used to define how the object behaves when we use the len() function with it.
# measur the length of the object, for example, the number of items in a list or the number of characters in a string.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __len__(self):
        return len(self.name)
Person = person('Anuj', 20)
print(len(Person)) # 4

# 7. __getitem__: this method is used to define how the object behaves when we use the indexing operator [] with it.
#  allows your object to behave like a list, string, tuple, or dictionary.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __getitem__(self,index):
        return self.name[index]
Person = person('Anuj', 20)
print(Person[0]) # A

# 8. __contains__: this method is used to define how the object behaves when we use the in operator with it.
# The method checks whether "A" exists inside self.name.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __contains__(self,item):
        return item in self.name
Person = person('Anuj', 20)
print('A' in Person) # True

# 9. __call__: this method is used to define how the object behaves when we call it like a function.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __call__(self):
        return f"{self.name} is {self.age} years old"
Person = person('Anuj', 20)
print(Person()) # Anuj is 20 years old

# 10. __iter__: this method is used to define how the object behaves when we use the iter() function with it.
# The method returns an iterator object that can be used to iterate over the elements of the object
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __iter__(self):
        return iter(self.name)
Person = person('Anuj', 20)
for char in Person:
    print(char) # A n u j

# 11. __bool__: this method is used to define how the object behaves when we use the bool() function with it.
# The method returns a boolean value that indicates whether the object is considered true or false.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __bool__(self):
        return self.age > 18
Person = person('Anuj', 20)
print(bool(Person)) # True

# 12. __del__: this method is used to define how the object behaves when it is deleted using the del statement.
class person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def __del__(self):
        print(f"{self.name} is deleted")
Person = person('Anuj', 20)
del Person # Anuj is deleted

# Write Money class with __eq__, __hash__, __repr_
class Money:
    def __init__(self,name, age, withdraw,deposit):
        self.name = name
        self.age  = age
        self.withdraw = withdraw
        self.deposit = deposit

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age and self.withdraw == other.withdraw and self.deposit == other.deposit

    def __hash__(self):
        return hash((self.name, self.age, self.withdraw, self.deposit))
    def __repr__(self):
        return f"Money('{self.name}', {self.age}, {self.withdraw}, {self.deposit})"

Person1 = Money('Anuj', 20, 1000, 500)
Person2 = Money('Anuj', 20, 1000, 500)
print(Person1 == Person2) # True
print(hash(Person1)) # 1234567890 (the hash value will be different each time)
print(repr(Person1)) # Money('Anuj', 20, 1000

# Write Playlist class with __len__, __getitem__, __iter__

class Playlist:
    def __init__(self,name,songs):
        self.name = name
        self.songs = songs
    def __len__(self):
        return len(self.songs)
    def __getitem__(self,index):
        return self.songs[index]
    def __iter__(self):
        return iter(self.songs)
playlist = Playlist('My Playlist', ['Song 1', 'Song 2', 'Song 3'])
print(len(playlist)) # 3
print(playlist[0]) # Song 1
for song in playlist:
    print(song) # Song 1, Song 2, Song 3
