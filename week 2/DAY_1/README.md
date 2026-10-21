# Week 2, Day 1: Functions, Scope, Closures, and Late Binding

This folder builds the ideas that make Python closures possible. Read the
files in this order:

1. [`first_class_func.py`](./first_class_func.py) — functions are values.
2. [`variable_in_scope.py`](./variable_in_scope.py) — how Python finds names.
3. [`closures_demo.py`](./closures_demo.py) — functions that remember values.
4. [`late_binding.py`](./late_binding.py) — why closures created in loops can
   surprise you.

The folder also contains this guide. It explains each file, the expected
behavior, practical uses, common mistakes, and exercises.

## Learning goals

By the end of this lesson, you should be able to:

- explain what it means for a function to be a first-class object;
- pass a function to another function and return a function;
- distinguish calling a function from referring to the function itself;
- explain local, enclosing, global, and built-in scopes;
- use `global` and `nonlocal` deliberately;
- identify a closure and explain what it remembers;
- build a function factory with a closure;
- keep private state in a closure;
- explain late binding in loops;
- fix late binding with a default argument, `functools.partial`, or a
  factory function; and
- decide whether a closure or a class is a clearer design.

## Running the examples

Run the closure example from the repository root:

```bash
python "week 2/DAY_1/closures_demo.py"
```

The other files are learning notebooks. They contain small examples placed
next to explanations, and some intentionally show an error or define a
function without calling it. Run them in sections while reading them.

To inspect a file without executing it:

```bash
python -m tokenize -e "week 2/DAY_1/late_binding.py"
```

To check syntax for all source files:

```bash
python -m py_compile \
  "week 2/DAY_1/first_class_func.py" \
  "week 2/DAY_1/variable_in_scope.py" \
  "week 2/DAY_1/closures_demo.py" \
  "week 2/DAY_1/late_binding.py"
```

## The big picture

These topics are connected:

```text
Functions are objects
        |
        v
Functions can be passed and returned
        |
        v
Nested functions can read enclosing variables
        |
        v
A returned nested function becomes a closure
        |
        v
Closures created in loops require care about late binding
```

The most important mental model is:

> A closure is a function together with the enclosing values it needs.

## 1. `first_class_func.py`: functions are values

### What “first-class function” means

In Python, a function is an object. Like strings, numbers, or lists, a
function can be:

- assigned to a variable;
- stored in a list, tuple, or dictionary;
- passed as an argument;
- returned from another function; and
- inspected with normal object operations such as `type()` and `__name__`.

This is different from calling a function. These two expressions do
different things:

```python
greet       # refers to the function object
greet("Anuj")  # calls the function and produces a result
```

The parentheses mean “execute it now”.

### Assigning a function to a variable

```python
def greet(name):
    return f"Hello, {name}!"

say_hello = greet
print(say_hello("Anuj"))
```

`say_hello` and `greet` refer to the same function object. Assigning the
function does not execute it and does not create a copy.

```python
print(say_hello is greet)  # True
```

### Storing functions in a data structure

```python
def add_one(number):
    return number + 1


def square(number):
    return number * number


operations = [add_one, square]
print(operations[0](4))  # 5
print(operations[1](4))  # 16
```

This is useful when the operation should be selected dynamically:

```python
operation_by_name = {
    "increase": add_one,
    "square": square,
}

selected_operation = operation_by_name["square"]
print(selected_operation(5))  # 25
```

### Passing a function as an argument

```python
def run_operation(operation, value):
    return operation(value)


print(run_operation(square, 6))  # 36
```

The function that accepts another function is often called a
**higher-order function**. Python's `sorted`, `map`, and `filter` are common
examples:

```python
names = ["anuj", "rohan", "simran"]
print(sorted(names, key=len))
print(list(map(str.upper, names)))
print(list(filter(lambda name: len(name) > 4, names)))
```

### Returning a function

```python
def make_power(exponent):
    def power(number):
        return number**exponent

    return power


square = make_power(2)
cube = make_power(3)
print(square(4))  # 16
print(cube(4))  # 64
```

This last pattern leads directly to closures. `power` uses `exponent` from
the enclosing `make_power` call.

### Important correction in the current file

The file contains this kind of call:

```python
def greet(name):
    return f"Hello, {name}!"


greeting = greet()
```

That raises:

```text
TypeError: greet() missing 1 required positional argument: 'name'
```

The corrected call is `greet("Anuj")`. The example is valuable because it
teaches the difference between a function reference (`greet`) and a function
call (`greet(...)`).

## 2. `variable_in_scope.py`: how Python finds names

### Local scope

A variable created inside a function is local to that function:

```python
def show_local_value():
    value = 10
    print(value)


show_local_value()
# print(value)  # NameError: value is not defined here
```

The local variable exists while the function is running and is not directly
available at module level.

### Global scope

A module-level variable is global to that module:

```python
message = "Hello from the module"


def show_message():
    print(message)


show_message()
print(message)
```

If Python cannot find a name locally, it searches the enclosing, global, and
then built-in scopes.

### Shadowing

An inner name can have the same spelling as an outer name:

```python
value = 30


def show_value():
    value = 40
    print(value)  # 40


show_value()
print(value)  # 30
```

The local `value` shadows the global `value` inside `show_value`; it does not
change the global variable.

### `global`

Use `global` when a function must rebind a module-level variable:

```python
total = 50


def replace_total():
    global total
    total = 60


replace_total()
print(total)  # 60
```

Avoid using `global` for ordinary application state when possible. It creates
hidden dependencies and makes testing harder. Prefer returning a new value,
passing state as an argument, using a closure, or using a class.

### Enclosing scope and `nonlocal`

An enclosing scope is the scope of an outer function around an inner
function:

```python
def make_counter():
    count = 0

    def next_count():
        nonlocal count
        count += 1
        return count

    return next_count
```

`nonlocal` means “rebind the variable in the nearest enclosing function
scope”. It does not mean global, and it cannot be used for a module-level
variable.

Without `nonlocal`, this fails:

```python
def make_counter():
    count = 0

    def next_count():
        count += 1  # UnboundLocalError

    return next_count
```

Because `count += 1` assigns to `count`, Python treats `count` as local to
`next_count` unless `nonlocal` says otherwise.

### Built-in scope

Python supplies names such as `len`, `print`, and `sum` in the built-in
scope:

```python
def show_builtin():
    print(len([10, 20, 30]))
```

Do not name your own variable `len`, `list`, or `sum` unless you deliberately
want to shadow the built-in. Shadowing can make later code confusing:

```python
list = [1, 2, 3]
# list("abc")  # TypeError: 'list' object is not callable
```

### LEGB lookup

Python generally looks for a name in this order:

| Letter | Scope | Example |
| --- | --- | --- |
| L | Local | Inside the current function |
| E | Enclosing | Inside an outer function |
| G | Global | At module level |
| B | Built-in | Names supplied by Python |

The first matching name wins.

## 3. `closures_demo.py`: functions that remember values

### Basic closure

```python
def make_greeting(name):
    def greeting():
        return f"Hello, {name}!"

    return greeting


say_hello = make_greeting("Anuj")
print(say_hello())  # Hello, Anuj!
```

`greeting` is nested, it reads `name` from the enclosing scope, and it is
returned. After `make_greeting` finishes, `say_hello` still has access to
`name`. That is a closure.

### Inspecting captured values

For learning, Python exposes closure cells:

```python
print(say_hello.__closure__)
print(say_hello.__closure__[0].cell_contents)
```

`__closure__` is an implementation-facing inspection tool. Normal code
should use the function's public behavior instead of changing closure cells.

### Independent closure instances

Each call to the outer function creates a separate enclosing environment:

```python
double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

`double` remembers `2`; `triple` remembers `3`. They do not share the
captured `factor`.

### Stateful closure with `nonlocal`

The `make_counter` example stores a private `count`:

```python
counter = make_counter(10)
print(counter())  # 11
print(counter())  # 12
```

The state is private by normal name lookup, and the returned function is the
only public operation in this small interface.

### Function factories

`make_multiplier` and `make_tax_calculator` are function factories. They
accept configuration once and return specialized functions:

```python
gst = make_tax_calculator(0.18)
print(gst(100))  # 118.0
```

Other factory examples include:

- a validator with a configured minimum length;
- a URL builder with a configured base URL;
- a converter with a configured unit;
- a retry function with a configured number of attempts; and
- a formatter with a configured date or currency style.

### Decorators are closures

`require_role("admin")` returns a decorator. The decorator returns a wrapper
that remembers both the required role and the original function:

```python
@require_role("admin")
def delete_record(record_id, *, user_role):
    return f"Deleted record {record_id}"
```

`functools.wraps` copies useful metadata such as the original function's
name and docstring. The Day 2 lesson expands this pattern.

### Callbacks

A callback can retain configuration:

```python
def make_handler(label):
    def handler(message):
        print(f"[{label}] {message}")

    return handler


error_handler = make_handler("ERROR")
error_handler("File not found")
```

This is useful for event handlers, request callbacks, task queues, and
pipeline steps.

## 4. `late_binding.py`: the loop-variable trap

### What late binding means

When a nested function refers to a free variable, Python looks up the
variable when the nested function is called. It does not automatically
freeze the value from the moment the function was created.

```python
functions = []
for number in range(3):
    functions.append(lambda: number)

print([function() for function in functions])  # [2, 2, 2]
```

All three lambdas refer to the same loop variable. The loop finishes with
`number == 2`, so all three calls read `2`.

This is sometimes called “late binding in a closure”. It is not that each
lambda receives a copy of `number`; each lambda performs a later name lookup.

### Fix 1: default argument

Default arguments are evaluated when the function is created:

```python
functions = [
    (lambda number=number: number)
    for number in range(3)
]

print([function() for function in functions])  # [0, 1, 2]
```

This is concise and idiomatic for simple cases.

### Fix 2: `functools.partial`

`partial` creates a callable with arguments pre-filled:

```python
from functools import partial


def multiply(number, factor):
    return number * factor


multipliers = [
    partial(multiply, factor=factor)
    for factor in range(4)
]

print([function(10) for function in multipliers])  # [0, 10, 20, 30]
```

Use `partial` when pre-binding arguments makes the intention clearer than a
lambda.

### Fix 3: factory function

An outer function gives every callback its own enclosing scope:

```python
def make_multiplier(factor):
    def multiply(number):
        return factor * number

    return multiply


multipliers = [make_multiplier(factor) for factor in range(4)]
print([function(10) for function in multipliers])  # [0, 10, 20, 30]
```

Use a factory when the callback needs multiple lines, validation, or more
than one captured value.

### Why late binding is useful

Late lookup is not always a bug. It allows a function to observe a changing
value:

```python
settings = {"prefix": "INFO"}


def log(message):
    print(settings["prefix"], message)


log("Started")  # INFO Started
settings["prefix"] = "DEBUG"
log("Started")  # DEBUG Started
```

The same runtime flexibility supports dynamic dispatch and polymorphism. The
important rule is to choose deliberately between a live lookup and a frozen
value.

## Closure versus class

Choose a closure when:

- the behavior is small and focused;
- only a few private values are needed; and
- one or two operations are enough.

Choose a class when:

- there are many related operations;
- state has several fields;
- a clear public API is needed;
- several instances need named methods; or
- inheritance or explicit object identity is useful.

Both can encapsulate state. Prefer the design that makes the public
interface easiest to understand and test.

## Current-file notes

The files are teaching notebooks rather than a production package:

- `first_class_func.py` includes an intentional incorrect `greet()` call
  without the required `name` argument. Read the corrected version above.
- `variable_in_scope.py` redefines names such as `func` and `outer_func` to
  demonstrate separate ideas. In a larger program, use distinct names.
- Some examples in `variable_in_scope.py` define functions without calling
  them. A definition alone produces no output.
- `late_binding.py` prints the incorrect result before showing three fixes.
  That incorrect result is part of the lesson.
- `closures_demo.py` is the cleanest complete runnable demonstration.

## Interactive exercises

Try each exercise before looking at the answer.

### Exercise 1: function as a value

Write `apply_twice(function, value)` so that this works:

```python
def add_one(number):
    return number + 1


assert apply_twice(add_one, 3) == 5
```

<details>
<summary>Answer</summary>

```python
def apply_twice(function, value):
    return function(function(value))
```

</details>

### Exercise 2: private counter

Write `make_counter(start)` so that:

```python
counter = make_counter(5)
assert counter() == 6
assert counter() == 7
```

<details>
<summary>Answer</summary>

```python
def make_counter(start):
    count = start

    def next_count():
        nonlocal count
        count += 1
        return count

    return next_count
```

</details>

### Exercise 3: closure inspection

Create a greeting closure and inspect its captured value using
`__closure__`. What type is `cell_contents`?

### Exercise 4: scope prediction

Before running this code, predict both outputs:

```python
value = "global"


def outer():
    value = "enclosing"

    def inner():
        print(value)

    inner()


outer()
print(value)
```

### Exercise 5: late binding

Fix this code in two different ways:

```python
functions = [lambda: number for number in range(4)]
```

The expected result is `[0, 1, 2, 3]`.

### Exercise 6: choose a design

Would you implement a shopping-cart total calculator as a closure or a
class? Explain what state and operations the object would need.

## Quick revision

| Concept | Meaning |
| --- | --- |
| First-class function | A function that can be stored, passed, and returned |
| Higher-order function | A function that accepts or returns a function |
| Local variable | A name inside the current function |
| Enclosing variable | A name in an outer function's scope |
| Global variable | A name at module level |
| `global` | Rebind a module-level name inside a function |
| `nonlocal` | Rebind a name in an enclosing function |
| Closure | Function plus remembered enclosing environment |
| Function factory | Function that returns a configured function |
| Late binding | Looking up a captured variable when the function runs |
| `partial` | Callable with some arguments pre-bound |

### Final self-check

You understand this lesson if you can explain:

1. why `greet` and `greet("Anuj")` are different;
2. why a local variable cannot normally be read outside its function;
3. why `nonlocal` is needed in `make_counter`;
4. what `make_multiplier(2)` returns;
5. why three lambdas in a loop can all return the same value; and
6. when a class is clearer than a closure.
