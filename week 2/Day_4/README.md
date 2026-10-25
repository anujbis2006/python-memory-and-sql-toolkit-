# Day 4: Iterables, Iterators, and Generators

This lesson explains how Python processes sequences one value at a time. The
main topics are:

- the difference between an iterable and an iterator,
- the `iter()` and `next()` functions,
- generator functions and the `yield` keyword,
- lazy evaluation and memory efficiency,
- how a `for` loop uses an iterator internally,
- sending values into a generator with `send()`, and
- stopping a generator and cleaning up with `close()`.

The examples are in [`generators_demo.py`](./generators_demo.py).

## 1. Iterable versus iterator

An **iterable** is an object whose values can be visited one at a time. Lists,
tuples, strings, sets, dictionaries, and many other Python objects are
iterables.

```python
numbers = [1, 2, 3]

for number in numbers:
    print(number)
```

The list is iterable because Python can create an iterator from it.

An **iterator** is the object that keeps track of the current position while
values are being read. An iterator implements:

- `__iter__()`, which returns the iterator itself, and
- `__next__()`, which returns the next value.

The built-in `iter()` function creates an iterator from an iterable:

```python
numbers = [1, 2, 3]
iterator = iter(numbers)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
```

After the last value has been returned, another call to `next()` raises
`StopIteration`:

```python
try:
    print(next(iterator))
except StopIteration:
    print("There are no more values")
```

An iterable can usually produce a fresh iterator each time. An iterator is
stateful and is normally consumed only once:

```python
numbers = [1, 2, 3]

first_iterator = iter(numbers)
second_iterator = iter(numbers)

print(next(first_iterator))   # 1
print(next(second_iterator))  # 1
```

Both iterators start at the beginning because they maintain separate state.

## 2. How a `for` loop works

This loop:

```python
for number in numbers:
    print(number)
```

behaves conceptually like this:

```python
iterator = iter(numbers)

while True:
    try:
        number = next(iterator)
    except StopIteration:
        break

    print(number)
```

The `for` loop automatically:

1. Calls `iter()` on the iterable.
2. Calls `next()` repeatedly.
3. Executes the loop body for every returned value.
4. Stops when `StopIteration` is raised.

This is why a `for` loop can work with lists, generators, files, and many
other objects that follow Python's iteration protocol.

## 3. Generator functions

A **generator function** is a function containing one or more `yield`
statements:

```python
def my_generator():
    yield 1
    yield 2
    yield 3
```

Calling a generator function does not run its body immediately. It returns a
generator object:

```python
generator = my_generator()
print(generator)
```

The body starts running when `next()` is called:

```python
print(next(generator))  # 1
print(next(generator))  # 2
print(next(generator))  # 3
```

When execution reaches a `yield`, Python:

1. Produces the yielded value.
2. Pauses the function at that exact location.
3. Saves its local variables and execution state.
4. Resumes from that location on the next `next()` call.

After the final `yield`, the generator is exhausted and raises
`StopIteration`.

The `yield` keyword is different from `return`. A `return` ends a normal
function permanently. A `yield` pauses a generator so that it can continue
later.

## 4. Generators are lazy

Generators use **lazy evaluation**. They produce a value only when the caller
requests one.

```python
def count_up_to(limit):
    number = 1
    while number <= limit:
        yield number
        number += 1
```

Creating the generator does not calculate all the values:

```python
numbers = count_up_to(1_000_000)
```

Only the requested value is created:

```python
print(next(numbers))  # 1
print(next(numbers))  # 2
```

This differs from a list:

```python
numbers_list = list(range(1_000_001))
numbers_generator = (number for number in range(1_000_001))
```

The list stores all values at once. The generator stores the logic and its
current state, producing values as needed.

Generators are especially useful for:

- large data sets,
- reading large files,
- processing database results,
- data pipelines,
- streams of events, and
- values that may not have a known final size.

Lazy evaluation does not automatically make every program faster. It mainly
reduces memory usage and allows work to be performed incrementally.

## 5. List versus generator in the example

The file defines two functions that create person records:

```python
def people_list(num_people):
    result = []
    for i in range(num_people):
        person = {
            "id": i,
            "name": random.choice(names),
            "major": random.choice(majors),
        }
        result.append(person)
    return result
```

This function creates every record and stores all records in `result` before
returning.

The generator version is:

```python
def people_generator(num_people):
    for i in range(num_people):
        person = {
            "id": i,
            "name": random.choice(names),
            "major": random.choice(majors),
        }
        yield person
```

It returns a generator immediately. Each person is created only when the
caller asks for the next record:

```python
people = people_generator(1_000_000)

first_person = next(people)
```

The generator version avoids holding one million dictionaries in memory at
the same time. If the caller eventually consumes every value, the total
amount of work can be similar to the list version, but the peak memory usage
can be much lower.

## 6. Generator expressions

A generator expression is the lazy equivalent of a list comprehension:

```python
 squares_list = [number * number for number in range(10)]
 squares_generator = (number * number for number in range(10))
```

The list expression creates all results immediately. The generator expression
creates results as they are requested.

Generator expressions are useful when the expression is short. For more
complex logic, a named generator function is usually easier to read and
reuse.

## 7. Sending values into a generator

Generators can receive values through the `send()` method. The value passed to
`send()` becomes the result of the paused `yield` expression.

```python
def my_generator():
    value = yield "Ready"
    print("Received:", value)
    yield "Finished"
```

Usage:

```python
generator = my_generator()

print(next(generator))       # Ready
print(generator.send(100))   # Received: 100, then Finished
```

The first `next()` call is necessary because the generator must reach its
first `yield` before it can receive a value. Calling `send(100)` on a
generator that has not started raises an error. To start it while sending
`None`, use `next(generator)` or `generator.send(None)`.

The sequence is:

1. `next(generator)` starts the function.
2. `yield "Ready"` pauses and produces `"Ready"`.
3. `send(100)` resumes the function.
4. The paused `yield` expression evaluates to `100`.
5. The function prints the received value and yields `"Finished"`.

`send()` is useful for coroutine-like code, feedback loops, and generators
that calculate their next output from input received from the caller.

## 8. Closing a generator

The `close()` method stops a generator before it naturally finishes:

```python
def my_generator():
    try:
        yield "First item"
        yield "Second item"
        yield "Third item"
    finally:
        print("Generator stopped and cleanup executed")


generator = my_generator()
print(next(generator))  # First item
generator.close()
```

Calling `close()` raises `GeneratorExit` inside the generator. A `finally`
block runs during this process, making it the correct place for cleanup such
as closing a file or releasing a resource.

Expected output:

```text
First item
Generator stopped and cleanup executed
```

After `close()`, the generator cannot produce more values. Calling `next()`
again raises `StopIteration`.

Do not normally catch `GeneratorExit` and continue yielding values. A
generator should use `finally` for cleanup and then allow the close operation
to complete.

## 9. Important differences at a glance

| Feature | Iterable | Iterator | Generator |
|---|---|---|---|
| Can be used in a `for` loop | Yes | Yes | Yes |
| Produces an iterator with `iter()` | Usually | Returns itself | Returns itself |
| Keeps iteration position | Usually no | Yes | Yes |
| Supports `next()` directly | Not always | Yes | Yes |
| Usually consumed once | No | Yes | Yes |
| Uses lazy evaluation | Not necessarily | Often | Yes |
| Common examples | List, tuple, string | `iter(list)` | Function with `yield` |

Every generator is an iterator. Not every iterator is a generator, and not
every iterable is an iterator.

## 10. Problems in the current source file

The source file is useful for studying the concepts, but some lines use old
or unavailable code:

1. `import mem_profile` requires an external module that is not part of the
   Python standard library. The program will fail at import time unless that
   dependency is installed and available.
2. `time.clock()` was removed from Python 3.8. Use `time.perf_counter()` for
   measuring elapsed time:

   ```python
   start = time.perf_counter()
   # work
   elapsed = time.perf_counter() - start
   ```

3. The memory comparison assigns `people` but does not consume the generator.
   That is intentional when demonstrating lazy creation, but it does not
   compare the time required to process all records. To measure full
   consumption, iterate over the generator.
4. The comments contain sample memory values. Actual measurements depend on
   the operating system, Python version, process state, and installed
   libraries, so those values should not be treated as guaranteed results.
5. `from itertools import count` is imported but not used in the current
   examples.

These issues do not change the main concepts: `iter()` creates iterators,
`next()` requests values, `yield` pauses generator functions, and generators
allow lazy, incremental processing.

## 11. Practical example: reading a large file

A file object is iterable. It produces one line at a time instead of
requiring the entire file to be loaded into memory:

```python
def non_empty_lines(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                yield line


for line in non_empty_lines("data.txt"):
    print(line)
```

The `with` block ensures that the file is closed after iteration finishes.
This combines generator laziness with reliable resource cleanup.

## 12. Summary

The key ideas from Day 4 are:

1. An iterable can provide values to an iterator.
2. An iterator remembers its current position and supplies values through
   `next()`.
3. A `for` loop uses `iter()`, repeated `next()` calls, and
   `StopIteration` internally.
4. A generator function contains `yield` and returns a lazy generator object.
5. `yield` pauses execution and preserves local state.
6. Generators reduce peak memory usage by producing one value at a time.
7. `send()` resumes a generator and supplies a value to its paused `yield`.
8. `close()` stops a generator and allows `finally` cleanup to run.
9. Every generator is an iterator, but not every iterator is a generator.

Once these ideas are understood, generators become a natural tool for
building memory-efficient data-processing pipelines.
