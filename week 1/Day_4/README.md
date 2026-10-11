# Day 4: Iterables, Iterators, and Generators

Welcome to Week 1, Day 4 of the Python learning series. This folder contains
[`iterator.py`](./iterator.py), a lesson about how Python moves through
sequences and how generators can produce values lazily.

The lesson connects four ideas:

1. An **iterable** is something Python can loop over.
2. An **iterator** remembers the current position while producing values.
3. `iter()` creates an iterator and `next()` asks it for the next value.
4. A **generator** is a convenient, lazy way to create an iterator.

Read each section, run the small examples, and answer the check-yourself
questions before continuing.

## Learning path

- [ ] Distinguish an iterable from an iterator.
- [ ] Create an iterator with `iter()`.
- [ ] Retrieve values with `next()`.
- [ ] Understand `StopIteration`.
- [ ] Understand how a `for` loop uses an iterator.
- [ ] Create a generator function with `yield`.
- [ ] Understand how `yield` pauses and resumes execution.
- [ ] Compare a list with a generator.
- [ ] Understand lazy evaluation and memory usage.
- [ ] Measure memory and execution time responsibly.

## A quick mental model

Think of an iterable as a book and an iterator as a bookmark:

- The **book** contains the values and can provide a fresh reading position.
- The **bookmark** remembers where you currently are.
- Calling `next()` moves the bookmark forward and returns the next value.

One iterable can create multiple independent iterators:

```python
numbers = [1, 2, 3]

first_reader = iter(numbers)
second_reader = iter(numbers)
```

Each iterator has its own position. A list can be iterated over again, but a
particular iterator is consumed as values are requested.

## Running the examples

The first sections of the source file use only Python's standard library:

```bash
python "week 1/Day_4/iterator.py"
```

However, the complete file contains two legacy dependencies:

```python
import mem_profile
...
t1 = time.clock()
```

`mem_profile` is not a standard-library module, and `time.clock()` was removed
from modern Python versions. Therefore the complete script may fail before the
memory benchmark runs. The concepts in the first sections can still be learned
independently, and the corrected benchmark pattern is included below.

For modern Python, use:

```python
import time
import tracemalloc
```

or install and use a maintained memory-measurement tool appropriate for your
environment. Use `time.perf_counter()` instead of `time.clock()`.

## 1. What is an iterable?

An iterable is an object that can return its items one at a time. Common
iterables include:

- Lists
- Tuples
- Strings
- Sets
- Dictionaries
- Files
- Generator objects

```python
numbers = [1, 2, 3, 4, 5]

for number in numbers:
    print(number)
```

The list is iterable, so Python can obtain an iterator from it and read its
values one at a time.

An iterable does not necessarily have to be an iterator itself. A list stores
its items and can create a new iterator whenever iteration begins.

## 2. What is an iterator?

An iterator is an object that produces values one at a time and remembers its
current position. It follows Python's iterator protocol:

- `__iter__()` returns an iterator.
- `__next__()` returns the next value.
- `__next__()` raises `StopIteration` when there are no values left.

Create an iterator from a list with `iter()`:

```python
numbers = [1, 2, 3, 4, 5]
iterator = iter(numbers)
```

Then request values with `next()`:

```python
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
```

Each call advances the same iterator. The next call continues from the
iterator's current position.

<details>
<summary>Check yourself</summary>

What is the difference between `numbers` and `iterator` in the example?

<details>
<summary>Answer</summary>

`numbers` is the iterable containing all five values. `iterator` is the
stateful object that remembers which value should be returned next.

</details>
</details>

## 3. `StopIteration`: the end of an iterator

After all values have been consumed, calling `next()` again raises
`StopIteration`:

```python
numbers = [1, 2]
iterator = iter(numbers)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # StopIteration
```

`StopIteration` is not normally shown when using a `for` loop because the loop
handles it internally. It means “there are no more values.”

You can handle it manually:

```python
iterator = iter([1, 2])

while True:
    try:
        value = next(iterator)
    except StopIteration:
        break
    print(value)
```

This is essentially the mechanism behind a `for` loop.

## 4. How a `for` loop works

This code:

```python
for number in numbers:
    print(number)
```

can be understood conceptually as:

```python
iterator = iter(numbers)

while True:
    try:
        number = next(iterator)
    except StopIteration:
        break
    print(number)
```

The actual interpreter implementation is optimized, but the model is
important:

1. Python calls `iter(numbers)`.
2. Python calls `next(iterator)`.
3. The returned value is assigned to `number`.
4. The loop body runs.
5. Steps 2–4 repeat.
6. `StopIteration` ends the loop.

That is why any object that follows the iteration protocol can work in a
`for` loop.

## 5. Iterators are consumed

An iterator is usually a one-pass stream:

```python
numbers = [1, 2, 3]
iterator = iter(numbers)

print(list(iterator))  # [1, 2, 3]
print(list(iterator))  # []
```

The first `list(iterator)` consumes all remaining values. The second call sees
an exhausted iterator.

To iterate over the original list again, create a new iterator:

```python
print(list(iter(numbers)))  # [1, 2, 3]
```

This difference matters when passing iterators between functions. A function
that consumes an iterator changes what the next function can read.

## 6. Generators

A generator is a special kind of iterator. The easiest way to create one is a
generator function containing `yield`:

```python
def my_generator():
    yield 1
    yield 2
    yield 3
```

Calling the function does not immediately run all three lines:

```python
generator = my_generator()
```

Instead, it returns a generator object. Values are produced when requested:

```python
print(next(generator))  # 1
print(next(generator))  # 2
print(next(generator))  # 3
```

The Day 4 file demonstrates exactly this pattern.

## 7. What `yield` does

`yield` has two important effects:

1. It produces a value for the caller.
2. It pauses the function at that point.

When `next()` is called again, execution resumes immediately after the previous
`yield`:

```python
def steps():
    print("before first value")
    yield 1
    print("before second value")
    yield 2
    print("finished")


values = steps()
print(next(values))
print(next(values))
```

The output is conceptually:

```text
before first value
1
before second value
2
```

The `"finished"` line runs only if the generator is advanced again, at which
point it ends and raises `StopIteration`.

This pause-and-resume behavior lets a generator retain local variables and
continue where it stopped.

<details>
<summary>Check yourself</summary>

Does calling `my_generator()` immediately produce the values `1`, `2`, and
`3`?

<details>
<summary>Answer</summary>

No. It creates a generator object. The function body runs as values are
requested with `next()` or by a loop.

</details>
</details>

## 8. Generator expressions

Generator expressions provide a compact syntax:

```python
squares = (number * number for number in range(5))

print(next(squares))  # 0
print(next(squares))  # 1
```

Compare this with a list comprehension:

```python
square_list = [number * number for number in range(5)]
square_generator = (number * number for number in range(5))
```

The list comprehension creates all values immediately. The generator
expression creates values as they are requested.

Use a generator when you need a stream of values and do not need all of them in
memory at the same time. Use a list when you need repeated access, indexing,
or the complete collection immediately.

## 9. List versus generator

The lesson defines a function that builds a complete list:

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

This function creates every dictionary and stores every dictionary in `result`
before returning.

The generator version uses `yield`:

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

Calling the two functions has different behavior:

```python
people = people_list(10)
people_stream = people_generator(10)
```

- `people` is a list containing all ten dictionaries.
- `people_stream` is a generator that has not created all ten dictionaries yet.

To consume the generator:

```python
for person in people_stream:
    print(person)
```

## 10. Lazy evaluation

Lazy evaluation means work is delayed until the result is needed.

This generator can represent a very large sequence:

```python
def count_up_to(limit):
    number = 1
    while number <= limit:
        yield number
        number += 1
```

Only the next requested value needs to be created:

```python
for number in count_up_to(3):
    print(number)
```

The generator does not build a list containing every number from `1` through
`limit`. This can reduce memory use when processing large or unbounded data.

Lazy evaluation does not make the data free. The values still require time to
be produced, and a generator cannot provide arbitrary indexes without
advancing through earlier values.

## 11. Memory behavior

The Day 4 file compares:

```python
people = people_list(1000000)
```

with:

```python
people = people_generator(1000000)
```

The list version stores one million dictionaries immediately. The generator
version stores the recipe and current state, then creates one dictionary at a
time as iteration requests it.

The rough memory pattern is:

```text
list      -> input data + all generated records
generator -> input data + generator state + current record
```

The generator is not automatically faster. It can be slower if values must be
regenerated or if the consumer needs to traverse the stream repeatedly. Its
main advantage is delayed work and lower peak memory for one-pass processing.

## 12. Measuring memory

The source attempts to use:

```python
import mem_profile
mem_profile.memory_usage_psutil()
```

`mem_profile` is not part of Python's standard library. The file does not
include that module, so a clean environment will usually raise
`ModuleNotFoundError`.

A modern, self-contained teaching alternative uses `tracemalloc`:

```python
import tracemalloc


def measure_memory(function, *args):
    tracemalloc.start()
    function(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current, peak
```

For operating-system process memory, use a maintained package and follow its
current documentation. Whichever tool you use, compare the list and generator
under the same conditions.

### What makes a fair comparison?

- Use the same number of records.
- Use the same input data and random seed when appropriate.
- Measure list creation and generator consumption separately.
- Repeat the measurement.
- Run in the same Python process configuration.
- Report the Python version and operating system.

Memory measurements are observations from one environment, not permanent
constants.

## 13. Measuring execution time

The lesson attempts to measure elapsed time with:

```python
t1 = time.clock()
...
t2 = time.clock()
```

`time.clock()` was removed in Python 3.8. For elapsed wall-clock timing, use:

```python
start = time.perf_counter()
result = function()
elapsed = time.perf_counter() - start
```

`time.perf_counter()` is designed for measuring short durations. For repeated
microbenchmarks, prefer `timeit`:

```python
import timeit

elapsed = timeit.timeit(
    "sum(range(1000))",
    number=1000,
)
```

Do not compare a list that has already been built with a generator that has
not been consumed. Decide whether you want to measure creation, consumption,
or both.

## 14. A corrected benchmark pattern

This example keeps the Day 4 idea while using modern timing and avoiding the
removed `time.clock()` function:

```python
import time


def consume(values):
    return sum(1 for _ in values)


start = time.perf_counter()
people = people_list(100_000)
list_creation_time = time.perf_counter() - start

start = time.perf_counter()
count = consume(people_generator(100_000))
generator_total_time = time.perf_counter() - start

print(f"List creation: {list_creation_time:.4f} seconds")
print(f"Generator creation and consumption: {generator_total_time:.4f} seconds")
print(f"Records consumed: {count}")
```

This measures two different workflows honestly:

- Building a complete list.
- Creating and consuming a generator in one pass.

For a complete comparison, also measure consuming the already-created list.

## 15. Why generators help with large data

Generators are useful for:

- Reading large files line by line.
- Processing database rows in batches.
- Streaming API responses.
- Transforming data pipelines.
- Producing infinite sequences.
- Stopping early after finding a result.

Example:

```python
def non_empty_lines(file_name):
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            if line:
                yield line
```

This does not load the entire file into memory. Each line is processed as it
is requested.

## 16. Generator pipelines

Generators can be connected:

```python
def numbers():
    for number in range(10):
        yield number


def even_numbers(values):
    for value in values:
        if value % 2 == 0:
            yield value


def doubled(values):
    for value in values:
        yield value * 2


pipeline = doubled(even_numbers(numbers()))

for value in pipeline:
    print(value)
```

The values travel through the pipeline one at a time. No intermediate list is
required.

This style is powerful, but remember that the pipeline is consumed once. If
you need to use the results more than once, materialize them with `list()` or
create a fresh pipeline.

## Interactive practice

Try each challenge before opening the answer.

### Challenge 1: create a countdown generator

Create a generator that yields numbers from `start` down to `1`.

<details>
<summary>One possible answer</summary>

```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1
```

</details>

### Challenge 2: consume only the first three values

Create a generator for a large range, but print only the first three values.

<details>
<summary>One possible answer</summary>

```python
values = (number for number in range(1_000_000))

for _ in range(3):
    print(next(values))
```

</details>

### Challenge 3: write a custom iterator

Create a class that counts from `start` to `stop`.

<details>
<summary>One possible answer</summary>

```python
class Counter:
    def __init__(self, start, stop):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.stop:
            raise StopIteration

        value = self.current
        self.current += 1
        return value
```

Usage:

```python
for number in Counter(1, 3):
    print(number)
```

</details>

### Challenge 4: filter people lazily

Write a generator that yields only people whose major is `"Engineering"`.

<details>
<summary>One possible answer</summary>

```python
def engineering_people(people):
    for person in people:
        if person["major"] == "Engineering":
            yield person
```

</details>

### Challenge 5: repair the timing code

Replace the removed `time.clock()` calls with a modern timer.

<details>
<summary>One possible answer</summary>

```python
start = time.perf_counter()
result = people_list(10_000)
elapsed = time.perf_counter() - start
print(elapsed)
```

</details>

## Common mistakes

### Calling `next()` on a list

This fails:

```python
next([1, 2, 3])
```

A list is iterable but is not itself an iterator. Use:

```python
next(iter([1, 2, 3]))
```

### Expecting an iterator to restart

Once an iterator is exhausted, calling `next()` does not start it again.
Create a new iterator or call the generator function again.

### Building a list from a generator immediately

This consumes and materializes the entire generator:

```python
values = list(large_generator())
```

That may be correct, but it removes the generator's memory advantage.

### Using `return` instead of `yield`

`return` ends a normal function. `yield` produces a value and pauses a
generator so it can resume later.

### Comparing unfair workloads

Measure list creation against generator creation and consumption, not list
creation against an unused generator object.

### Using outdated timing APIs

Use `time.perf_counter()` or `timeit`, not `time.clock()` in modern Python.

### Forgetting external dependencies

`mem_profile` is not a built-in module. Install or replace it before running
the benchmark section.

## Quick reference

| Concept | Syntax | Meaning |
|---|---|---|
| Iterable | `for item in value` | Can provide values for iteration |
| Create iterator | `iter(value)` | Get a stateful iterator |
| Get next value | `next(iterator)` | Advance and return one value |
| End of iteration | `StopIteration` | No values remain |
| Generator function | `def function(): yield value` | Defines lazy iteration |
| Generator expression | `(expression for item in values)` | Compact lazy iterator |
| Materialize values | `list(iterator)` | Consume into a list |
| High-resolution timer | `time.perf_counter()` | Measure elapsed time |
| Repeated benchmark | `timeit.timeit(...)` | Measure repeated code |

## Summary

Day 4 explains the mechanism behind Python loops and lazy data processing:

1. An iterable can provide an iterator.
2. An iterator remembers its position and returns one value at a time.
3. `iter()` creates an iterator and `next()` advances it.
4. `StopIteration` signals that an iterator is exhausted.
5. A `for` loop repeatedly calls `next()` until iteration ends.
6. `yield` pauses a generator and resumes it on the next request.
7. Lists create and store all values immediately.
8. Generators produce values lazily and can reduce peak memory usage.
9. Generators are usually one-pass streams.
10. Memory and timing comparisons must use modern tools and fair workloads.
