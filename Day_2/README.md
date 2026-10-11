# Day 2: Python Decorators

Welcome to Day 2 of the Python learning series. This folder contains one
example file, [`decorators_basic.py`](./decorators_basic.py), that builds the
idea of a decorator step by step.

The lesson is designed to be read and executed interactively. Read one
section, find the matching example in the Python file, run it, and then answer
the short check-yourself question before moving on.

## Learning path

- [ ] Understand how an inner function can remember an outer variable.
- [ ] Build a decorator manually.
- [ ] Use the `@decorator` syntax.
- [ ] Pass arguments through a decorator with `*args` and `**kwargs`.
- [ ] Create a decorator with a class and `__call__`.
- [ ] Add logging and timing behavior.
- [ ] Understand why decorator order matters.
- [ ] Preserve function metadata with `functools.wraps`.

## What is a decorator?

A decorator is a callable that receives a function, adds behavior around that
function, and returns a callable that can be used in its place.

```python
def announce(function):
    def wrapper():
        print("Before the function")
        function()
        print("After the function")
    return wrapper


@announce
def greet():
    print("Hello")


greet()
```

The `@announce` line is shorthand for:

```python
greet = announce(greet)
```

The original `greet` function is passed to `announce`, and the returned
`wrapper` becomes the new value of `greet`.

## Run the lesson

From the repository root:

```bash
python Day_2/decorators_basic.py
```

Or, from inside the Day 2 folder:

```bash
cd Day_2
python decorators_basic.py
```

The complete file contains several demonstrations, so it prints multiple
messages and sleeps for approximately one second in the timing examples.
Because the logging decorator is also used, running the file can create a
`display_info.log` file in the current working directory. That file is runtime
output, not part of the lesson source.

## 1. Closures: a function remembering its environment

The first example defines `outer_function()` and an `inner_function()` inside
it. The inner function uses `message`, even after `outer_function()` has
returned:

```python
def outer_function():
    message = "Hi"

    def inner_function():
        print(message)

    return inner_function
```

When `my_func = outer_function()` runs, `my_func` receives the returned inner
function. Calling `my_func()` prints `Hi`.

This is a **closure**: the inner function keeps access to variables from the
scope where it was created. Decorators use this same idea to remember the
function they are wrapping.

<details>
<summary>Check yourself</summary>

Why can `inner_function()` still read `message` after
`outer_function()` has finished?

<details>
<summary>Answer</summary>

The returned function closes over the surrounding scope, so Python keeps the
needed value available to it.

</details>
</details>

## 2. Building a decorator by hand

The first `decorator_function()` accepts `original_function`, defines a
`wrapper_function()`, and returns the wrapper:

```python
def decorator_function(original_function):
    def wrapper_function():
        print("Wrapper function executed before the original function")
        return original_function()

    return wrapper_function
```

It can be used without `@` syntax:

```python
decorated_display = decorator_function(display)
decorated_display()
```

The call sequence is:

1. `display` is passed into `decorator_function`.
2. `wrapper_function` is returned.
3. Calling `decorated_display()` runs the wrapper.
4. The wrapper runs the original `display` function.

This lets us add behavior without editing the body of `display`.

## 3. The `@decorator` syntax

Python provides a shorter and clearer form:

```python
@decorator_function
def display():
    print("Display function ran")
```

This means the same thing as:

```python
display = decorator_function(display)
```

The name `display` now refers to the wrapper returned by the decorator.

## 4. Forwarding function arguments

A wrapper with no parameters can only wrap functions that also take no
arguments. The Day 2 file demonstrates the problem with `display_info(name,
age)`.

The general solution is:

```python
def wrapper_function(*args, **kwargs):
    return original_function(*args, **kwargs)
```

- `*args` collects positional arguments into a tuple.
- `**kwargs` collects keyword arguments into a dictionary.
- Passing them again with `*args` and `**kwargs` forwards the original call.

This makes the decorator reusable with functions that have different
signatures.

## 5. Class-based decorators

The lesson also implements a decorator as a class:

```python
class decorator_class:
    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        print("Wrapper class executed before the original function")
        return self.original_function(*args, **kwargs)
```

An instance becomes callable because it defines `__call__`. Therefore this:

```python
@decorator_class
def display():
    print("Display function ran")
```

is equivalent to storing the original function inside a `decorator_class`
instance. Calling `display()` invokes that instance, which then calls the
stored function.

Use a function decorator for simple wrapping. A class-based decorator is
useful when the decorator needs to keep state between calls.

## 6. Logging and timing decorators

### `my_logger`

`my_logger` configures Python's `logging` module and records the positional and
keyword arguments used for each call:

```python
logging.info("Ran with args: {}, and kwargs: {}".format(args, kwargs))
```

The log message is written to a file named after the decorated function, such
as `display_info.log`.

### `my_timer`

`my_timer` records the time before and after the original function runs:

```python
t1 = time.time()
result = orig_func(*args, **kwargs)
t2 = time.time() - t1
```

It prints the elapsed time and returns `result`. Returning the result is
important: a decorator should not accidentally replace a function's useful
return value with `None`.

## 7. Stacking decorators and order of execution

Decorators can be stacked:

```python
@my_timer
@my_logger
def display_info(name, age):
    ...
```

Decorators are applied from the bottom upward. The example above is equivalent
to:

```python
display_info = my_timer(my_logger(display_info))
```

Reversing the order changes which wrapper receives the call first and can
change the output and logging behavior:

```python
@my_logger
@my_timer
def display_info(name, age):
    ...
```

When debugging stacked decorators, expand the `@` syntax into assignments and
trace the call from the outside wrapper toward the original function.

## 8. Preserving metadata with `functools.wraps`

Without extra help, wrapping a function changes useful metadata. For example,
`display_info.__name__` may become `"wrapper"` instead of `"display_info"`.

The final section imports `wraps` and uses it inside each decorator:

```python
from functools import wraps


def my_timer(orig_func):
    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        ...

    return wrapper
```

`@wraps(orig_func)` copies important metadata such as the original function's
name and docstring to the wrapper. This improves debugging, documentation, and
introspection while keeping the decorator behavior unchanged.

## Try it yourself

After reading the file, create a small decorator that counts calls:

```python
from functools import wraps


def count_calls(function):
    calls = 0

    @wraps(function)
    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print(f"{function.__name__} call #{calls}")
        return function(*args, **kwargs)

    return wrapper
```

Apply it to a function, call that function three times, and verify that the
counter increases. Then try combining it with `my_timer` from the lesson.

### Practice questions

1. What does `@my_timer` become when written without decorator syntax?
2. Why does a wrapper usually return the result of the original function?
3. What is the difference between `*args` and `**kwargs`?
4. What changes when two decorators are written in the opposite order?
5. What problem does `@wraps(orig_func)` solve?

## Key takeaways

- A decorator wraps a function to add reusable behavior.
- A closure allows the wrapper to remember the original function.
- `@decorator` is shorthand for replacing a function with a decorated value.
- `*args` and `**kwargs` let a wrapper forward flexible arguments.
- A class can act as a decorator when it implements `__call__`.
- Stacked decorators are applied from the bottom upward.
- `functools.wraps` preserves the wrapped function's metadata.
