# Day 5: Context Managers in Python

This lesson explains **context managers**: Python objects that prepare a
resource before a block of code runs and reliably clean it up afterward.

The examples in [`context_demo.py`](./context_demo.py) use context managers
for:

- opening and closing files,
- temporarily changing the current working directory,
- understanding the `with` statement,
- implementing `__enter__` and `__exit__`, and
- creating context managers with `contextlib.contextmanager`.

By the end of this guide, you should be able to explain why this code is safer
than manually opening and closing a resource:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Context managers are useful.")
```

## 1. The resource-management problem

Some operations acquire resources that must eventually be released:

- opening a file,
- connecting to a database,
- acquiring a thread lock,
- opening a network connection,
- changing the current working directory, or
- starting and stopping a transaction.

Without a context manager, cleanup has to be written manually:

```python
file = open("notes.txt", "w", encoding="utf-8")
try:
    file.write("Hello")
finally:
    file.close()
```

The `finally` block is important because it runs whether the work succeeds or
raises an exception. However, repeating this pattern everywhere is easy to
forget or implement incorrectly.

A context manager packages the setup and cleanup behavior:

```python
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Hello")
```

The file is closed automatically when the `with` block ends, including when an
exception occurs inside the block.

## 2. Understanding the `with` statement

This statement:

```python
with resource_manager() as resource:
    use(resource)
```

has this conceptual flow:

1. Create the context manager.
2. Call its `__enter__()` method.
3. Assign the value returned by `__enter__()` to `resource`.
4. Run the indented block.
5. Call `__exit__()` when the block finishes.

The `as resource` variable is not automatically the context manager object.
It is whatever value `__enter__()` returns. For a file, it is the opened file
object. For a custom class, it might be `self`, a connection, or another
helper object.

Conceptually:

```python
manager = resource_manager()
resource = manager.__enter__()
try:
    use(resource)
finally:
    manager.__exit__(None, None, None)
```

The real language behavior passes exception information to `__exit__()` when
an exception occurs, which allows the context manager to clean up and decide
whether the exception should continue.

## 3. A class-based context manager

A class becomes a context manager when it defines `__enter__()` and
`__exit__()`:

```python
class OpenFile:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding="utf-8")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
```

It can then be used with `with`:

```python
with OpenFile("test.txt", "w") as file:
    file.write("Hello, World!")

print(file.closed)  # True
```

### `__enter__`

`__enter__()` runs when execution enters the `with` block. It should:

- acquire or prepare the resource,
- save anything needed for cleanup, and
- return the object that the block should use.

In the example, the method opens the file and returns the file object.

### `__exit__`

`__exit__()` runs when execution leaves the block. It should release the
resource:

```python
def __exit__(self, exc_type, exc_value, traceback):
    self.file.close()
```

The method receives three exception-related arguments:

| Argument | Meaning |
|---|---|
| `exc_type` | The exception class, or `None` if no exception occurred |
| `exc_value` | The exception instance, or `None` |
| `traceback` | The traceback object, or `None` |

The names are conventional; they can be different, but the three positions
are required.

## 4. Exceptions and the return value of `__exit__`

By default, an exception raised inside a `with` block should continue to the
caller after cleanup. Returning `False` or `None` from `__exit__()` preserves
that behavior:

```python
class ManagedResource:
    def __enter__(self):
        print("Acquired")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Released")
        return False
```

To deliberately suppress an exception, `__exit__()` must return `True`:

```python
class IgnoreValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return exc_type is ValueError


with IgnoreValueError():
    raise ValueError("This is suppressed")

print("Execution continues")
```

Suppressing exceptions should be rare and intentional. A context manager that
silently hides unexpected failures can make debugging difficult. Cleanup code
should not turn a failed operation into a false success unless that behavior
is part of the documented API.

Even when an exception is raised, cleanup must still happen:

```python
with OpenFile("test.txt", "w") as file:
    file.write("Before the error")
    raise RuntimeError("Something failed")
```

`__exit__()` closes the file before the `RuntimeError` is reported.

## 5. Function-based context managers

Writing a class for every small context manager can be verbose. The
`contextlib.contextmanager` decorator allows a generator function to define
the same setup and cleanup pattern:

```python
from contextlib import contextmanager


@contextmanager
def open_file(filename, mode):
    file = open(filename, mode, encoding="utf-8")
    try:
        yield file
    finally:
        file.close()
```

Usage:

```python
with open_file("simple.txt", "w") as file:
    file.write("Hello, World!")

print(file.closed)  # True
```

The function is divided by `yield` into two sections:

```text
before yield  -> setup
yield value   -> value assigned after `as`
after yield   -> cleanup
```

For the example:

1. Code before `yield` opens the file.
2. `yield file` gives the file to the `with` block.
3. The block runs.
4. The `finally` block closes the file.

The `finally` block is essential. If it were omitted, an exception inside the
`with` block could leave the file open.

### Why `yield` is used here

This is not a normal generator that the caller repeatedly consumes. The
`contextmanager` decorator converts the generator function into a context
manager. The single `yield` marks the boundary between setup and the body of
the `with` block.

## 6. Temporarily changing the working directory

`context_demo.py` also demonstrates a context manager that changes the
current working directory and restores it afterward:

```python
import os
from contextlib import contextmanager


@contextmanager
def change_dir(destination):
    original_directory = os.getcwd()
    os.chdir(destination)
    try:
        yield
    finally:
        os.chdir(original_directory)
```

Usage:

```python
with change_dir("Sample-Dir-Two"):
    print(os.listdir())

print(os.getcwd())  # Back to the original directory
```

This pattern is useful when a small operation must run relative to a
particular directory, but the rest of the application should not be affected.

The restoration belongs in `finally`, because the directory must be restored
even if the block raises an exception:

```python
with change_dir("Sample-Dir-Two"):
    raise RuntimeError("The operation failed")

# The original directory has still been restored.
```

Changing the process-wide working directory can affect other code running in
the same process. Keep the context short, and prefer absolute paths when that
is clearer or when multiple tasks may run concurrently.

## 7. A second class-based example

The final example in the source file focuses on the lifecycle rather than
performing real file I/O:

```python
class File:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"Opening file: {self.name}....")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Closing file: {self.name}....")


with File("test.txt") as file:
    print(f"Working with file: {file.name}....")

print("Done!")
```

Expected output:

```text
Opening file: test.txt....
Working with file: test.txt....
Closing file: test.txt....
Done!
```

This makes the order easy to observe:

```text
__enter__() -> with-block -> __exit__()
```

The `if __name__ == "__main__":` guard in the source file ensures that this
demonstration runs when the file is executed directly, but not when it is
imported as a module.

## 8. Interactive prediction exercises

Read each example before looking at the answer. Predict the output and
identify when cleanup occurs.

### Exercise A: lifecycle order

```python
class Demo:
    def __enter__(self):
        print("enter")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit")


with Demo():
    print("body")
```

<details>
<summary>Show the answer</summary>

```text
enter
body
exit
```

</details>

### Exercise B: cleanup after an exception

```python
try:
    with Demo():
        print("body")
        raise ValueError("failed")
except ValueError:
    print("handled")
```

<details>
<summary>Show the answer</summary>

```text
enter
body
exit
handled
```

`__exit__()` runs before the exception reaches the `except` block.

</details>

### Exercise C: what does `as` receive?

```python
class Demo:
    def __enter__(self):
        return "value from enter"

    def __exit__(self, exc_type, exc_value, traceback):
        pass


with Demo() as result:
    print(result)
```

<details>
<summary>Show the answer</summary>

```text
value from enter
```

The variable after `as` receives the return value of `__enter__()`, not
automatically the `Demo` instance.

</details>

### Exercise D: exception suppression

Change the following `__exit__()` method to suppress only `KeyError`:

```python
def __exit__(self, exc_type, exc_value, traceback):
    ...
```

<details>
<summary>Show the answer</summary>

```python
def __exit__(self, exc_type, exc_value, traceback):
    return exc_type is KeyError
```

Returning `True` for a `KeyError` suppresses it. Returning `False` or `None`
for every other exception allows it to propagate.

</details>

## 9. Practice tasks

Try these exercises after reading the examples:

1. Create a `Timer` context manager that prints how many seconds the block
   took. Use `time.perf_counter()`.
2. Create a `temporary_directory(path)` context manager that changes to
   `path` and always restores the original directory.
3. Create a `transaction` context manager with `begin`, `commit`, and
   `rollback` behavior. Commit when the block succeeds and roll back when it
   raises an exception.
4. Rewrite the `open_file` function as a class with `__enter__` and
   `__exit__`.
5. Add an exception type check to a context manager and decide explicitly
   whether it should suppress that exception.
6. Nest two context managers and write down the order in which their
   `__enter__` and `__exit__` methods execute.

Nested contexts enter from the outside inward and exit in reverse order:

```python
with Outer():
    with Inner():
        print("work")
```

The lifecycle is:

```text
Outer.__enter__
Inner.__enter__
work
Inner.__exit__
Outer.__exit__
```

## 10. Notes about the current source file

The concepts are correct, but the demonstration assumes that two directories
already exist:

```text
Sample-Dir-One
Sample-Dir-Two
```

If they do not exist in the directory from which the script is run,
`os.chdir()` raises `FileNotFoundError`. Create those directories first or
replace the examples with paths that exist on your machine.

The file also creates `test.txt` and `simple.txt` in write mode. Running the
script can therefore create or overwrite those files. This is expected for a
demonstration, but use temporary paths when experimenting with important
data.

For production file code, specify an encoding:

```python
open(filename, mode, encoding="utf-8")
```

The source file's `open_File` class does not currently pass an encoding, and
the class name would conventionally be written as `OpenFile` in Python's
`CapWords` style. These are readability improvements, not changes to the
context-manager protocol.

## 11. Context-manager checklist

When creating a context manager, ask:

- What resource or state is acquired?
- What should `__enter__()` return?
- What must always be cleaned up?
- Is cleanup inside `finally`?
- Should exceptions propagate or be intentionally suppressed?
- Does `__exit__()` handle partial setup safely?
- Can the resource be used concurrently?
- Would `contextlib.contextmanager` make the code clearer?

## 12. Summary

The most important ideas from Day 5 are:

1. A context manager controls setup and cleanup around a `with` block.
2. The `with` statement calls `__enter__()` on entry and `__exit__()` on exit.
3. `__enter__()` returns the value bound after `as`.
4. `__exit__()` receives exception information and runs even when the block
   fails.
5. Returning `True` from `__exit__()` suppresses the exception; returning
   `False` or `None` lets it propagate.
6. `@contextmanager` turns a generator function into a context manager.
7. Code before `yield` is setup, and code in `finally` is cleanup.
8. Context managers are useful for files, directories, locks, databases,
   network resources, and temporary state.

The central rule is simple: **acquire in setup, use inside `with`, and always
release in cleanup**.
