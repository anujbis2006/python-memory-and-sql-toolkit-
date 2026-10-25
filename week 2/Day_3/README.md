# Day 3: Decorators with Arguments and Caching

This lesson explains how to create decorators that accept configuration
arguments. It also introduces a practical rate limiter and the idea behind an
LRU (Least Recently Used) cache.

The examples in [`decorators_args.py`](./decorators_args.py) are intended to
show two important ideas:

1. A decorator factory can receive settings before it receives the function
   that will be decorated.
2. Decorators can store state, such as call timestamps or cached values,
   inside a closure.

> **Important:** `decorators_args.py` currently contains a few mistakes that
> prevent it from running exactly as written. The intended behavior and fixes
> are explained below.

## 1. What is a decorator?

A decorator is a callable that receives a function, adds behavior around that
function, and returns a replacement function.

```python
def simple_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before the function")
        result = func(*args, **kwargs)
        print("After the function")
        return result

    return wrapper


@simple_decorator
def greet(name):
    return f"Hello, {name}"
```

This syntax:

```python
@simple_decorator
def greet(name):
    ...
```

is equivalent to:

```python
def greet(name):
    ...


greet = simple_decorator(greet)
```

The decorator receives the original `greet` function and replaces it with the
returned `wrapper`.

## 2. Why do we need a decorator factory?

A normal decorator receives only the function:

```python
@simple_decorator
def function():
    ...
```

Sometimes the decorator itself needs configuration:

```python
@rate_limiter(max_calls=3, time_window=10, error_message="Too fast!")
def request_api_data():
    ...
```

Here, the values `3`, `10`, and `"Too fast!"` are not arguments to
`request_api_data`. They configure the decorator. A function that accepts
those configuration values and returns a decorator is called a **decorator
factory**.

## 3. The three levels of a decorator factory

A decorator factory has three nested function levels:

```python
def factory(configuration):          # Level 1: receives configuration
    def decorator(func):             # Level 2: receives the target function
        def wrapper(*args, **kwargs):  # Level 3: receives call arguments
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

Each level has a separate responsibility:

### Level 1: Factory

The outer function receives configuration such as:

- a maximum number of calls,
- a time window,
- a retry count,
- a cache size, or
- a custom error message.

It does not receive the target function yet.

### Level 2: Decorator

The middle function receives the function being decorated. It can create
state that belongs to that decorated function and return the wrapper.

### Level 3: Wrapper

The innermost function runs every time the decorated function is called. It
can inspect the call arguments, apply the configured behavior, call the
original function, and return its result.

The evaluation order is useful to remember:

```python
@factory(option=value)
def work():
    ...
```

is equivalent to:

```python
work = factory(option=value)(work)
```

The first call creates the decorator. The second call applies that decorator
to `work`.

## 4. Rate limiter example

The file implements a rate limiter using this structure:

```python
def rate_limiter(max_calls, time_window, error_message):
    def decorator(func):
        call_timestamps = []

        def wrapper(*args, **kwargs):
            nonlocal call_timestamps
            current_time = time.time()

            call_timestamps = [
                timestamp
                for timestamp in call_timestamps
                if current_time - timestamp < time_window
            ]

            if len(call_timestamps) >= max_calls:
                raise PermissionError(error_message)

            call_timestamps.append(current_time)
            return func(*args, **kwargs)

        return wrapper

    return decorator
```

Usage:

```python
@rate_limiter(
    max_calls=3,
    time_window=10.0,
    error_message="Too fast!",
)
def request_api_data(user_id):
    return f"API request made for {user_id}"
```

### How the rate limiter works

1. The factory stores the configured limit, time window, and error message.
2. The decorator creates one `call_timestamps` list for the decorated
   function.
3. Every call records the current time.
4. Timestamps older than the configured time window are removed.
5. If the number of remaining timestamps is already equal to the limit, the
   call is rejected.
6. Otherwise, the current timestamp is saved and the original function runs.

The `nonlocal` statement is important here. The wrapper reassigns
`call_timestamps` after removing expired timestamps, so it must tell Python to
use the variable from the enclosing `decorator` function rather than create a
new local variable.

Example:

```python
print(request_api_data("Alice"))  # Call 1: allowed
print(request_api_data("Alice"))  # Call 2: allowed
print(request_api_data("Alice"))  # Call 3: allowed
print(request_api_data("Alice"))  # Call 4: PermissionError
```

This is a simple in-memory limiter. In a real multi-process application, the
timestamps would usually be stored in shared infrastructure such as Redis,
because each process would otherwise have its own separate list.

## 5. LRU caching

Caching saves the result of an expensive operation so that repeated calls with
the same input can return quickly.

**LRU** means **Least Recently Used**. When a cache reaches its maximum size,
the item that has not been used for the longest time is removed.

The file uses `collections.OrderedDict` to implement the cache:

```python
from collections import OrderedDict


class SimpleLRUCache:
    def __init__(self, max_size):
        self.max_size = max_size
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
```

`OrderedDict` keeps insertion order. The implementation treats the end of
the dictionary as the most recently used side:

- `get()` moves an accessed item to the end.
- `put()` moves an updated item to the end.
- `popitem(last=False)` removes the first item, which is the least recently
  used item.

## 6. Correct way to use the custom cache

`SimpleLRUCache` is a cache object, not a decorator. Therefore this is
incorrect:

```python
@SimpleLRUCache(max_size=3)
def get_data_from_db(query):
    ...
```

An instance of `SimpleLRUCache` is not callable because it does not define a
`__call__` method. A decorator adapter can connect the cache object to a
function:

```python
import time
from functools import wraps


def lru_cache_decorator(max_size):
    def decorator(func):
        cache = SimpleLRUCache(max_size)

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            result = cache.get(key)

            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.put(key, result)
            return result

        return wrapper

    return decorator


@lru_cache_decorator(max_size=3)
def get_data_from_db(query):
    time.sleep(1)
    return f"Results for {query}"
```

The first call for a query performs the slow operation. A later call with the
same arguments gets the stored result. The key includes positional and
keyword arguments so different calls can have different cached results.

For production code, Python already provides a tested implementation:

```python
from functools import lru_cache


@lru_cache(maxsize=3)
def get_data_from_db(query):
    time.sleep(1)
    return f"Results for {query}"
```

Arguments used with `lru_cache` must be hashable. Lists and dictionaries
cannot be used directly as cached arguments.

## 7. Errors to fix in the current example

The concepts are useful, but the current source file needs these corrections
before it can run:

1. `mac_calls` is likely a typo for `max_calls`. It works only if the same
   misspelled name is used consistently, but `max_calls` is clearer.
2. `return f"API request made" {user_id}` is invalid Python syntax. It should
   be:

   ```python
   return f"API request made for {user_id}"
   ```

3. `request_api_data()` is defined without a parameter but called with
   `"Alice"`. Either define it as `request_api_data(user_id)` or call it
   without an argument.
4. `@SimpleLRUCache(max_size=3)` applies a non-callable cache object as a
   decorator. Use a decorator adapter such as `lru_cache_decorator`, or use
   `functools.lru_cache`.
5. The cache wrapper should use `*args` and `**kwargs` if the decorated
   function accepts both positional and keyword arguments.
6. A cached function should return a value that clearly represents a cache
   miss. Using `None` as the miss marker means that caching a legitimate
   `None` result needs additional handling.

## 8. Summary

The main lesson is that adding parentheses to a decorator changes its
structure:

```python
@decorator
def function():
    ...
```

uses a two-level decorator:

```text
decorator -> wrapper
```

while:

```python
@decorator(configuration)
def function():
    ...
```

uses a three-level decorator factory:

```text
factory -> decorator -> wrapper
```

Once this structure is understood, the same pattern can be used for retry
logic, rate limiting, logging, authorization, timing, validation, and
caching.
