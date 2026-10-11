# Day 3: Dataclasses, Object Memory, and `__slots__`

Welcome to Week 1, Day 3 of the Python learning series. This folder contains
[`memory_compare.py`](./memory_compare.py), a practical lesson about making
classes easier to write and comparing the memory cost of normal Python
objects with classes that use `__slots__`.

The lesson connects three ideas:

1. How Python objects are created and compared.
2. How `@dataclass` generates useful class methods for us.
3. How `__slots__` can reduce per-instance memory overhead.

Read each section, run the matching code, and answer the check-yourself
questions before continuing.

## Learning path

- [ ] Understand that each object has its own identity.
- [ ] Use `id()` to inspect object identity.
- [ ] Understand why two separate instances are not automatically equal.
- [ ] Use `@dataclass` to generate class methods.
- [ ] Understand dataclass field ordering and defaults.
- [ ] Understand `frozen=True`.
- [ ] Understand `order=True`.
- [ ] Use `field(init=False, repr=False)`.
- [ ] Understand the purpose of `__post_init__`.
- [ ] Compare a normal class with a slotted class.
- [ ] Understand why `__slots__` removes `__dict__`.
- [ ] Measure memory and timing instead of guessing about performance.

## Requirements

The first object and dataclass examples use only the Python standard library.
The memory comparison uses `memory_profiler`:

```bash
python -m pip install memory-profiler
```

Run the lesson from the repository root:

```bash
python "week 1/Day_3/memory_compare.py"
```

Or from inside this folder:

```bash
cd "week 1/Day_3"
python memory_compare.py
```

The script creates one million objects in each memory experiment and repeats
the measurements ten times. It can therefore take a while and use a
substantial amount of memory. Close other memory-heavy applications before
running the complete file.

## 1. Every object has an identity

The first class stores a person's name, job, and age:

```python
class Person:
    name: str
    job: str
    age: str

    def __init__(self, name: str, job: str, age: str):
        self.name = name
        self.job = job
        self.age = age
```

Creating three objects creates three separate instances:

```python
person1 = Person("Anuj", "Software Engineer", "20")
person2 = Person("Jennifer", "Software Engineer", "34")
person3 = Person("alexa", "Software Engineer", "45")
```

The built-in `id()` function returns an integer identifying an object during
its lifetime:

```python
print(id(person1))
print(id(person2))
```

The exact values are implementation-dependent and can change between runs.
Do not treat an `id()` value as a permanent database ID.

### Identity is different from equality

This comparison is false:

```python
print(person3 == person2)
```

The two objects are different instances. A normal class does not automatically
compare all of its attributes for value equality. Without a custom `__eq__`,
the comparison is based on object identity.

These are different questions:

| Expression | Question |
|---|---|
| `person1 is person2` | Are these the exact same object? |
| `person1 == person2` | Do these objects compare as equal? |
| `id(person1)` | What identity number does this object have now? |

<details>
<summary>Check yourself</summary>

If two `Person` objects have the same name, job, and age, are they necessarily
the same object?

<details>
<summary>Answer</summary>

No. They can contain the same values while still being two separate objects.
`is` checks identity, while `==` checks the class's equality behavior.

</details>
</details>

## 2. What `@dataclass` does

Writing `__init__`, `__repr__`, and `__eq__` by hand can become repetitive.
The `@dataclass` decorator can generate common methods from type-annotated
fields:

```python
from dataclasses import dataclass


@dataclass
class Person:
    name: str
    job: str
    age: str
```

The decorator can generate methods such as:

- `__init__` for assigning fields.
- `__repr__` for readable object output.
- `__eq__` for field-by-field equality.
- `__hash__` in configurations where hashing is safe.
- Ordering methods when `order=True` is enabled.

The Day 3 file uses:

```python
@dataclass(order=True, frozen=True)
class Person:
    ...
```

This asks dataclasses to generate ordering methods and make instances
immutable.

### Generated representation

The dataclass representation looks similar to:

```text
Person(name='Anuj', job='Software Engineer', age='20', strength=100)
```

This is more useful for debugging than the default representation of a normal
class.

### Generated equality

Two dataclass instances with the same field values compare equal:

```python
first = Person("Anuj", "Software Engineer", "20")
second = Person("Anuj", "Software Engineer", "20")

print(first == second)  # True
```

Dataclass equality is based on the declared fields and normally requires the
objects to be instances of the same dataclass type.

## 3. Dataclass fields and defaults

The Day 3 class declares:

```python
class Person:
    sort_index: int = field(init=False, repr=False)

    name: str
    job: str
    age: str
    strength: int = 100
```

### `field(init=False)`

`init=False` means callers do not provide `sort_index` in the generated
constructor:

```python
person = Person("Anuj", "Software Engineer", "20")
```

The caller supplies `name`, `job`, and `age`; `sort_index` is intended to be
calculated later.

### `field(repr=False)`

`repr=False` excludes `sort_index` from the generated `repr()` output. This is
useful for an internal helper field that should affect ordering but does not
need to be shown to users.

### Default values

`strength: int = 100` gives every new object a default strength of `100`
unless another value is explicitly provided:

```python
strong_person = Person(
    "Anuj",
    "Software Engineer",
    "20",
    strength=120,
)
```

Dataclass field order matters. Fields without defaults must come before fields
with defaults. That is why `strength` is declared after `name`, `job`, and
`age`.

## 4. `frozen=True`: immutable dataclass instances

The `frozen=True` option prevents normal attribute assignment after an object
has been created:

```python
person = Person("Anuj", "Software Engineer", "20")

# This raises dataclasses.FrozenInstanceError:
# person.age = "21"
```

Frozen objects are useful when their values should not change after creation.
They are also safer candidates for hashing because a key's fields should not
change while it is stored in a set or dictionary.

`frozen=True` does not mean that every object reachable from a field is deeply
immutable. If a frozen dataclass contains a mutable list, the list itself may
still be changed unless you design around that.

<details>
<summary>Check yourself</summary>

Why is immutability useful for an object used as a dictionary key?

<details>
<summary>Answer</summary>

Dictionary lookup uses the object's hash and equality. If fields used by those
methods change after insertion, the dictionary may no longer find the key in
the expected hash bucket.

</details>
</details>

## 5. `order=True`: generated comparisons

With `order=True`, dataclasses can generate:

- `__lt__` for `<`
- `__le__` for `<=`
- `__gt__` for `>`
- `__ge__` for `>=`

The comparisons use fields in their declaration order unless a field is
excluded from comparison:

```python
first > second
```

is evaluated using the generated ordering methods.

### Field order matters

The class declares `sort_index` before the visible fields. The purpose is to
make ordering use a numeric sort value before comparing the other fields.
That is why the lesson attempts to initialize it from the person's age.

However, the current source names the method:

```python
def __post__init__(self):
```

The dataclass hook is named:

```python
def __post_init__(self):
```

Because of this spelling difference, Python does not automatically call the
method in the current file. The README explains the intended dataclass
pattern, while the existing script demonstrates the current source exactly.

For the intended behavior, the method would be:

```python
def __post_init__(self):
    object.__setattr__(self, "sort_index", int(self.age))
```

The `object.__setattr__` call is needed because `frozen=True` prevents ordinary
assignment. It is safe here during controlled initialization.

The current example also stores `age` as a `str`. If age is used for numeric
ordering, converting it to `int` for `sort_index` is important.

## 6. `__post_init__`: post-construction processing

`__post_init__` is an optional dataclass hook. Dataclasses call it immediately
after the generated `__init__` finishes:

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Person:
    name: str
    age: str
    sort_index: int = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "sort_index", int(self.age))
```

This is useful for:

- Converting or validating input.
- Calculating derived fields.
- Normalizing values.
- Preparing fields that callers should not set directly.

The method name must be spelled exactly `__post_init__`. A method named
`__post__init__` is an ordinary method and will not be called automatically.

## 7. Why the order example can be surprising

The lesson prints:

```python
print(person1 > person2)
```

The comments describe sorting by age, but three details matter:

1. `__post__init__` is misspelled, so `sort_index` is not initialized by the
   dataclass hook.
2. `sort_index` is declared first, so it participates in ordering by default.
3. `age` is annotated as `str`, so direct comparison of age values would be
   lexicographic rather than numeric.

When teaching or extending this example, fix the hook spelling and explicitly
convert age to an integer. Then the ordering rule is clear and testable.

## 8. Normal classes have an instance `__dict__`

The lesson defines:

```python
class PointWithoutSlots:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

Instances normally have a `__dict__` containing their attributes:

```python
point = PointWithoutSlots(1, 2)
print(point.__dict__)
# {'x': 1, 'y': 2}
```

An instance dictionary is flexible. New attributes can be added later:

```python
point.color = "red"
```

That flexibility has memory overhead because each instance needs storage for
its dictionary and its attribute entries.

## 9. `__slots__`: fixed instance attributes

The slotted class declares its supported attributes explicitly:

```python
class PointWithSlots:
    __slots__ = ["x", "y"]

    def __init__(self, x, y):
        self.x = x
        self.y = y
```

This tells Python to store these attributes in a more compact layout and not
create a normal instance `__dict__`.

Therefore:

```python
point = PointWithSlots(1, 2)
print(point.__dict__)
```

raises an `AttributeError` because this class does not provide `__dict__`.

The following also fails:

```python
# AttributeError: 'PointWithSlots' object has no attribute 'color'
point.color = "red"
```

Only names listed in `__slots__` can be assigned.

### Benefits and trade-offs

| Normal class | Class with `__slots__` |
|---|---|
| Has an instance `__dict__` | Usually has no instance `__dict__` |
| New attributes can be added | Only declared attributes are allowed |
| More flexible | More memory-efficient for many small objects |
| Easy to extend dynamically | Requires deliberate attribute design |

`__slots__` is not automatically faster or always better. It is most useful
when a class has a fixed, known set of fields and many instances are created.

## 10. Measuring memory with `memory_profiler`

The lesson imports:

```python
from memory_profiler import memory_usage
```

It creates one million points:

```python
def create_points():
    return [PointWithoutSlots(i, i) for i in range(1000000)]
```

Then it samples memory while the function runs:

```python
mem_usage_without_slots = memory_usage(
    create_points,
    interval=0.01,
)
mem_values.append(max(mem_usage_without_slots))
```

The process is repeated ten times and the average is calculated:

```python
statistics.mean(mem_values)
```

The same experiment is repeated for `PointWithSlots`.

### Interpreting the results

The output is affected by the operating system, Python version, allocator,
background processes, and the measurement method. The values in comments are
examples, not guaranteed constants.

Use the measurement to compare the two designs in the same environment, not
as a universal promise that every slotted class will use a particular amount
of memory.

## 11. Measuring attribute-access time with `timeit`

The script also times repeated attribute reads:

```python
time_without_slots = timeit.timeit(
    lambda: (points.x, points.y),
    number=1000000,
)
```

`timeit.timeit` runs the expression many times and returns elapsed time in
seconds. Averaging ten runs reduces the impact of one unusual measurement.

Timing should be interpreted carefully:

- A microbenchmark is not the same as application performance.
- The Python version and machine affect the result.
- Memory savings may matter more than a tiny attribute-access difference.
- Measure your actual workload before optimizing.

## 12. Normal class versus slotted class

The two experiments use the same logical data:

```python
PointWithoutSlots(i, i)
PointWithSlots(i, i)
```

The difference is the storage model:

```text
PointWithoutSlots -> instance dictionary -> x and y
PointWithSlots    -> fixed slots          -> x and y
```

The slotted version can reduce per-object overhead when the program creates a
large number of small objects. The trade-off is reduced flexibility and extra
care when using inheritance or weak references.

## Interactive practice

Try each task before opening the answer.

### Challenge 1: add a formatted greeting

Add a method or property that returns:

```text
Anuj works as a Software Engineer
```

<details>
<summary>One possible answer</summary>

```python
def summary(self):
    return f"{self.name} works as a {self.job}"
```

</details>

### Challenge 2: use a numeric age

Change the dataclass field from `age: str` to `age: int`. What changes when
you create an object?

<details>
<summary>One possible answer</summary>

```python
@dataclass(order=True, frozen=True)
class Person:
    name: str
    job: str
    age: int
```

Then construct it with `age=20`, not `"20"`. Numeric comparisons now work
directly with the age field.

</details>

### Challenge 3: repair post-initialization

Fix the hook so `sort_index` is calculated automatically.

<details>
<summary>One possible answer</summary>

```python
def __post_init__(self):
    object.__setattr__(self, "sort_index", int(self.age))
```

</details>

### Challenge 4: add a slot

Add `z` to `PointWithSlots` and initialize it:

```python
point = PointWithSlots(1, 2, 3)
```

<details>
<summary>One possible answer</summary>

```python
class PointWithSlots:
    __slots__ = ["x", "y", "z"]

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
```

</details>

### Challenge 5: compare memory responsibly

Change the number of created points from `1_000_000` to `10_000`, run both
versions, and record the results. Then explain why your numbers should not be
copied as universal values.

<details>
<summary>Answer</summary>

Measurements depend on the Python version, operating system, allocator,
background processes, sampling interval, and hardware. The useful result is
the comparison made under the same conditions.

</details>

## Common mistakes

### Confusing identity and equality

Two objects can contain the same values without being the same object. Use
`is` for identity and `==` for value comparison.

### Misspelling `__post_init__`

The exact spelling is required. `__post__init__` is not the dataclass hook.

### Assuming `frozen=True` makes everything deeply immutable

Frozen dataclasses prevent reassignment of their fields, but nested mutable
objects can still be changed.

### Using `__slots__` without listing every attribute

An attribute not included in `__slots__` cannot be assigned unless the class
also provides another supported storage mechanism.

### Believing comments are measurement results

Memory and timing comments are examples. Run the benchmark in your own
environment and interpret the result in context.

### Running the full benchmark without checking dependencies

Install `memory-profiler` first, and remember that creating one million objects
can take significant memory and time.

## Quick reference

| Concept | Syntax or tool | Purpose |
|---|---|---|
| Object identity | `id(object)` | Inspect identity during its lifetime |
| Identity comparison | `a is b` | Check whether references point to one object |
| Dataclass | `@dataclass` | Generate common class methods |
| Frozen dataclass | `frozen=True` | Prevent normal field reassignment |
| Ordered dataclass | `order=True` | Generate ordering comparisons |
| Field configuration | `field(...)` | Customize constructor, repr, and comparison |
| Post-processing | `__post_init__` | Run after generated `__init__` |
| Normal attributes | `object.__dict__` | Store dynamic instance attributes |
| Fixed attributes | `__slots__` | Restrict fields and reduce overhead |
| Memory measurement | `memory_usage(...)` | Sample process memory |
| Timing measurement | `timeit.timeit(...)` | Measure repeated operations |

## Summary

Day 3 shows how Python gives us tools for both expressive classes and
performance-aware design:

1. Every object has an identity, and identity is different from equality.
2. `@dataclass` removes repetitive class boilerplate.
3. `frozen=True` protects field assignment after construction.
4. `order=True` generates comparison methods, but field order still matters.
5. `__post_init__` is the exact hook name for derived dataclass values.
6. `field(init=False, repr=False)` is useful for internal calculated fields.
7. Normal objects usually store dynamic attributes in `__dict__`.
8. `__slots__` provides a fixed attribute layout and can reduce memory use.
9. `memory_profiler` and `timeit` help replace guesses with measurements.
10. Benchmarks should be repeated and interpreted in the context of the actual
    application.
