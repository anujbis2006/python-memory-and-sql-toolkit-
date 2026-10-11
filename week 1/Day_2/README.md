# Day 2: Python Dunder Methods

Welcome to Week 1, Day 2 of the Python learning series. This folder contains
[`memory_compare.py`](./memory_compare.py), a practical introduction to
**dunder methods**, also called **magic methods** or **special methods**.

The name “dunder” comes from **double underscore**:

```text
__method__
```

These methods let a class define how its objects work with Python's built-in
operations. For example:

- `print(object)` can use `__str__`
- `object1 + object2` can use `__add__`
- `len(object)` can use `__len__`
- `object[index]` can use `__getitem__`
- `value in object` can use `__contains__`
- `object()` can use `__call__`

The lesson starts with small classes and finishes with two practical classes:
`Money` and `Playlist`.

## Learning path

- [ ] Understand what dunder methods are.
- [ ] Define an object's display text with `__str__`.
- [ ] Customize addition with `__add__`.
- [ ] Distinguish `__str__` from `__repr__`.
- [ ] Compare objects with `__eq__`.
- [ ] Make objects usable with `hash()`.
- [ ] Define length with `__len__`.
- [ ] Support indexing with `__getitem__`.
- [ ] Support membership checks with `__contains__`.
- [ ] Make an object callable with `__call__`.
- [ ] Make an object iterable with `__iter__`.
- [ ] Define truth-value behavior with `__bool__`.
- [ ] Understand the limitations of `__del__`.
- [ ] Combine dunder methods in reusable classes.

## What are dunder methods?

Python has built-in syntax that works with many different types:

```python
numbers = [1, 2, 3]

print(numbers)
print(len(numbers))
print(numbers[0])
print(2 in numbers)
```

Lists know how to respond to these operations because Python's data model
defines special methods for them.

When you write:

```python
len(numbers)
```

Python effectively asks the object for its length:

```python
numbers.__len__()
```

The exact implementation is handled by Python, but `__len__` is the method
that communicates this behavior.

> Dunder methods are normally called by Python through built-in syntax. You
> can call them directly while learning, but expressions such as `len(value)`
> and `value[index]` are usually clearer in application code.

## Running the example

From the repository root, use quotes because the folder name contains a space:

```bash
python "week 1/Day_2/memory_compare.py"
```

Or run it from inside the Day 2 folder:

```bash
cd "week 1/Day_2"
python memory_compare.py
```

The script prints the result of each demonstration. The exact integer returned
by `hash()` can vary between Python runs, so do not expect that line to have a
fixed number.

## 1. `__init__`: initialize an object

`__init__` runs after an object is created. It stores the values needed by the
object:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

When this line runs:

```python
person = Person("Anuj", 20)
```

Python creates a `Person` object and calls `__init__` to set `name` and `age`.
The method does not usually return the object; Python handles object creation
around it.

`__init__` is included in the lesson because nearly every custom class needs
some form of initialization.

## 2. `__str__`: user-friendly text

`__str__` controls the readable text produced by `str(object)` and commonly
by `print(object)`:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"


person = Person("Anuj", 20)
print(person)  # Anuj is 20 years old
```

Without `__str__`, printing a custom object usually shows a less useful
representation containing its class and memory address.

### Rule for `__str__`

`__str__` must return a string:

```python
def __str__(self):
    return "Readable object text"
```

Returning an integer or another object causes a `TypeError`.

<details>
<summary>Check yourself</summary>

What does `print(person)` use when `Person` defines `__str__`?

<details>
<summary>Answer</summary>

`print(person)` converts the object to text and uses the string returned by
`person.__str__()`.

</details>
</details>

## 3. `__add__`: customize the `+` operator

`__add__` defines what happens when two objects are added with `+`.
The lesson uses a `point` class:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"
```

Now two points can be added naturally:

```python
p1 = Point(1, 2)
p2 = Point(5, 5)
p3 = p1 + p2

print(p3)  # (6, 7)
```

Python interprets `p1 + p2` by calling the left object's addition behavior.
The method returns a **new** `Point`; it does not change `p1` or `p2`.

The example assumes that `other` has `x` and `y` attributes. A production
implementation could add a type check and raise a clear error for unsupported
operands.

## 4. `__repr__`: developer-friendly representation

`__repr__` defines the representation returned by `repr(object)`. It is
intended to be useful for debugging and inspecting objects:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


person = Person("Anuj", 20)
print(repr(person))  # Person('Anuj', 20)
```

### `__str__` versus `__repr__`

| Method | Main purpose | Common use |
|---|---|---|
| `__str__` | Friendly text for users | `print(object)` |
| `__repr__` | Detailed text for developers | `repr(object)` and debugging |

A useful `__repr__` often makes the object's important state obvious.

If a class does not define `__str__`, Python may fall back to `__repr__` for
some string conversions. They are still separate methods with different
communication goals.

## 5. `__eq__`: compare objects with `==`

`__eq__` defines equality:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age


person1 = Person("Anuj", 20)
person2 = Person("Anuj", 20)

print(person1 == person2)  # True
```

Without a custom `__eq__`, two separate instances are normally not equal just
because their attributes have the same values.

The lesson's implementation assumes that `other` is another compatible
`Person`. A safer version checks the type first:

```python
def __eq__(self, other):
    if not isinstance(other, Person):
        return NotImplemented
    return self.name == other.name and self.age == other.age
```

Returning `NotImplemented` lets Python try the other operand's comparison or
produce the appropriate result.

## 6. `__hash__`: use objects in hashed collections

`__hash__` defines the integer returned by `hash(object)`:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __hash__(self):
        return hash((self.name, self.age))
```

The tuple groups the values into one hashable value:

```python
hash((self.name, self.age))
```

Hashable objects can be used as dictionary keys or members of a set:

```python
people = {Person("Anuj", 20)}
```

### Important equality and hashing rule

If two objects compare equal, they must have the same hash:

```python
a == b  ->  hash(a) == hash(b)
```

Do not calculate a hash from fields that can change while the object is inside
a set or being used as a dictionary key. If the fields change, Python may no
longer be able to find the object in the correct hash bucket.

The number printed by `hash()` is not a stable ID and may differ between
processes.

## 7. `__len__`: define `len(object)`

`__len__` defines the result of the built-in `len()` function:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __len__(self):
        return len(self.name)


person = Person("Anuj", 20)
print(len(person))  # 4
```

Python effectively calls:

```python
person.__len__()
```

The method must return a non-negative integer. In this example, the chosen
meaning of length is “the number of characters in the name.”

`__len__` can also affect truth checks when `__bool__` is not defined:

```python
if person:
    print("The object has a non-zero length")
```

For a collection-like class, `__len__` should usually return the number of
items it contains.

## 8. `__getitem__`: support `object[index]`

`__getitem__` defines indexing and can also support slicing:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getitem__(self, index):
        return self.name[index]


person = Person("Anuj", 20)

print(person[0])    # A
print(person[-1])   # j
print(person[0:2])  # An
```

These expressions call:

```python
person.__getitem__(0)
person.__getitem__(-1)
person.__getitem__(slice(0, 2))
```

The Day 2 implementation forwards the index to `self.name`, so it behaves
like the name string. A list-backed class can use the same pattern:

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __getitem__(self, index):
        return self.songs[index]
```

## 9. `__contains__`: support the `in` operator

`__contains__` defines membership checks:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __contains__(self, item):
        return item in self.name


person = Person("Anuj", 20)

print("A" in person)  # True
print("z" in person)  # False
```

When Python evaluates:

```python
"A" in person
```

it can call:

```python
person.__contains__("A")
```

For a dictionary-like object, `__contains__` would usually check whether a key
exists in the internal dictionary:

```python
def __contains__(self, key):
    return key in self.data
```

`__contains__` should return a Boolean result.

## 10. `__call__`: make an object callable

`__call__` defines what happens when an object is followed by parentheses:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __call__(self):
        return f"{self.name} is {self.age} years old"


person = Person("Anuj", 20)
print(person())  # Anuj is 20 years old
```

`person()` is equivalent to:

```python
person.__call__()
```

This is useful for function-like objects that need to store state:

```python
class Counter:
    def __init__(self):
        self.value = 0

    def __call__(self):
        self.value += 1
        return self.value


counter = Counter()
print(counter())  # 1
print(counter())  # 2
```

`__call__` can accept arguments just like a normal function.

## 11. `__iter__`: make an object iterable

`__iter__` defines how an object produces an iterator:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __iter__(self):
        return iter(self.name)


person = Person("Anuj", 20)

for character in person:
    print(character)
```

The output is:

```text
A
n
u
j
```

The method returns `iter(self.name)`, an iterator over the characters in the
name. A `for` loop repeatedly asks that iterator for its next value until it
is exhausted.

For the `Playlist` class, `__iter__` returns an iterator over its songs:

```python
def __iter__(self):
    return iter(self.songs)
```

This allows the class to work with `for`, `list()`, and other iterable-aware
operations.

## 12. `__bool__`: define truth-value testing

`__bool__` defines the result of `bool(object)` and controls how an object
behaves in conditions:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __bool__(self):
        return self.age > 18


person = Person("Anuj", 20)
print(bool(person))  # True
```

Because the age is greater than 18, the object is truthy:

```python
if person:
    print("This person is an adult")
```

`__bool__` must return `True` or `False`. If `__bool__` is not defined,
Python may use `__len__`: zero means false and a non-zero length means true.

In real applications, choose a truth rule that is intuitive for the class.
For example, an empty `Playlist` could be false, while a valid configuration
object might always be true.

## 13. `__del__`: object finalization

The lesson demonstrates `__del__`:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __del__(self):
        print(f"{self.name} is deleted")


person = Person("Anuj", 20)
del person
```

The `del person` statement removes that name's reference to the object. If no
other references remain, Python may finalize the object and call `__del__`.

### Important warning

Do not use `__del__` as a reliable replacement for explicit resource cleanup.
Its timing can depend on Python's implementation, reference cycles, and
interpreter shutdown. For files, database connections, and locks, prefer
explicit cleanup or a context manager:

```python
with open("notes.txt") as file:
    contents = file.read()
```

The `__del__` example is useful for understanding object lifetime, but it is
not a general cleanup pattern.

## 14. The `Money` class: combining comparison, hashing, and representation

The lesson combines three methods in `Money`:

- `__eq__` compares all stored values.
- `__hash__` creates a hash from those values.
- `__repr__` shows the object's state.

```python
class Money:
    def __init__(self, name, age, withdraw, deposit):
        self.name = name
        self.age = age
        self.withdraw = withdraw
        self.deposit = deposit

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.age == other.age
            and self.withdraw == other.withdraw
            and self.deposit == other.deposit
        )

    def __hash__(self):
        return hash((self.name, self.age, self.withdraw, self.deposit))

    def __repr__(self):
        return f"Money('{self.name}', {self.age}, {self.withdraw}, {self.deposit})"
```

Two objects with matching values compare as equal:

```python
money1 = Money("Anuj", 20, 1000, 500)
money2 = Money("Anuj", 20, 1000, 500)

print(money1 == money2)  # True
print(repr(money1))     # Money('Anuj', 20, 1000, 500)
```

Because all fields used by equality are also used by hashing, the class follows
the important equality/hash relationship. In a production model, the fields
should also be treated as immutable while instances are used in sets or as
dictionary keys.

## 15. The `Playlist` class: collection-like behavior

The final example combines three collection behaviors:

```python
class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self.songs = songs

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __iter__(self):
        return iter(self.songs)
```

Now the playlist can be used like a collection:

```python
playlist = Playlist(
    "My Playlist",
    ["Song 1", "Song 2", "Song 3"],
)

print(len(playlist))  # 3
print(playlist[0])    # Song 1

for song in playlist:
    print(song)
```

The three methods have different jobs:

| Expression | Method | Result |
|---|---|---|
| `len(playlist)` | `__len__` | Number of songs |
| `playlist[0]` | `__getitem__` | First song |
| `for song in playlist` | `__iter__` | Each song in order |

This is the main design lesson: a class can provide a familiar interface by
implementing the special methods that match the operations users need.

## Quick reference

| Dunder method | Python operation | Role in this lesson |
|---|---|---|
| `__init__` | `Class(...)` | Initialize attributes |
| `__str__` | `str(object)`, `print(object)` | Friendly text |
| `__add__` | `object1 + object2` | Add two points |
| `__repr__` | `repr(object)` | Debug representation |
| `__eq__` | `object1 == object2` | Compare values |
| `__hash__` | `hash(object)` | Produce a hash value |
| `__len__` | `len(object)` | Define object length |
| `__getitem__` | `object[index]` | Retrieve an item |
| `__contains__` | `value in object` | Test membership |
| `__call__` | `object()` | Call an object like a function |
| `__iter__` | `iter(object)`, `for` | Provide iteration |
| `__bool__` | `bool(object)`, `if object` | Define truthiness |
| `__del__` | Object finalization | Demonstrate lifetime behavior |

## Interactive practice

Read one section at a time and try each challenge before opening its answer.

### Challenge 1: add a greeting

Add a `greeting()` method to `Person` that returns a message using the name.
Then compare it with the output from `__str__`.

<details>
<summary>One possible answer</summary>

```python
def greeting(self):
    return f"Hello, {self.name}!"
```

</details>

### Challenge 2: improve `Point.__add__`

What should happen when someone tries to add a `Point` to an integer? Add a
type check and raise a clear `TypeError`.

<details>
<summary>One possible answer</summary>

```python
def __add__(self, other):
    if not isinstance(other, Point):
        raise TypeError("Point can only be added to another Point")
    return Point(self.x + other.x, self.y + other.y)
```

</details>

### Challenge 3: add playlist membership

Make this expression work:

```python
"Song 2" in playlist
```

<details>
<summary>One possible answer</summary>

```python
def __contains__(self, song):
    return song in self.songs
```

</details>

### Challenge 4: make a playlist callable

Make `playlist()` return the playlist name and number of songs.

<details>
<summary>One possible answer</summary>

```python
def __call__(self):
    return f"{self.name}: {len(self)} songs"
```

</details>

### Challenge 5: test truthiness

Decide whether an empty playlist should be false:

```python
empty_playlist = Playlist("Empty", [])
print(bool(empty_playlist))
```

Try implementing `__bool__` with the rule “a playlist is true when it has at
least one song.”

<details>
<summary>One possible answer</summary>

```python
def __bool__(self):
    return len(self.songs) > 0
```

</details>

## Common mistakes

### Returning the wrong type from a dunder method

Some methods have strict return requirements:

- `__str__` and `__repr__` must return strings.
- `__len__` must return a non-negative integer.
- `__bool__` must return a Boolean.
- `__iter__` must return an iterator.

### Forgetting to return the original result

If `__add__` creates a new object, return it. If `__getitem__` retrieves an
item, return it. A missing return statement produces `None` and breaks the
expected operation.

### Making equality and hashing inconsistent

Objects that compare equal must have equal hashes. Use the same identity fields
for both `__eq__` and `__hash__`.

### Treating `__del__` as guaranteed cleanup

Object finalization is not a substitute for context managers or explicit
resource management.

### Using dunder methods only to be clever

Implement a dunder method when it makes the class easier and more natural to
use. A surprising `__add__` or `__bool__` can make code harder to understand.

## Summary

Dunder methods connect a class to Python's built-in language features. They let
custom objects feel natural without requiring callers to learn a separate
method for every operation.

The most important ideas from this lesson are:

1. `__str__` provides readable output.
2. `__repr__` provides useful debugging output.
3. `__eq__` defines value-based equality.
4. `__hash__` enables use in sets and dictionary keys when the object is safely
   hashable.
5. `__len__`, `__getitem__`, and `__iter__` make objects collection-like.
6. `__contains__` supports `in`.
7. `__call__` makes an instance behave like a function.
8. `__bool__` controls truth-value testing.
9. `__del__` demonstrates object lifetime but should not manage resources.
10. Dunder methods are the bridge between custom classes and Python syntax.
