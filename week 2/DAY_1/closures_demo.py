"""Practical examples of Python closures.

A closure is an inner function that remembers values from its enclosing
function even after the enclosing function has returned.
"""

from __future__ import annotations

from functools import wraps
from typing import Callable, TypeVar


ReturnType = TypeVar("ReturnType")


def make_greeting(name: str) -> Callable[[], str]:
    """Return a function that remembers ``name``."""

    def greeting() -> str:
        return f"Hello, {name}!"

    return greeting
# output - in this code we  see how closures work in python. 
# A closure is a function that remembers the values from its enclosing scope even after the outer function has finished executing. 
# In this code, we have several examples of closures, including a greeting function, a counter,
#  a multiplier, a tax calculator, and an authorization decorator. Each of these functions captures 
# variables from their enclosing scope and retains access to them even after the outer function has returned.

def make_counter(start: int = 0) -> Callable[[], int]:
    """Return a counter whose state is private to the returned function."""
    count = start

    def next_count() -> int:
        nonlocal count
        count += 1
        return count

    return next_count


def make_multiplier(factor: int) -> Callable[[int], int]:
    """Return a function that multiplies its input by ``factor``."""

    def multiply(number: int) -> int:
        return number * factor

    return multiply


def make_tax_calculator(rate: float) -> Callable[[float], float]:
    """Return a calculator that remembers a tax rate."""

    def calculate(price: float) -> float:
        return price * (1 + rate)

    return calculate


def require_role(required_role: str) -> Callable[
    [Callable[..., ReturnType]], Callable[..., ReturnType]
]:
    """Create a simple authorization decorator using a closure."""

    def decorator(
        function: Callable[..., ReturnType],
    ) -> Callable[..., ReturnType]:
        @wraps(function)
        def wrapper(*args: object, **kwargs: object) -> ReturnType:
            user_role = kwargs.get("user_role")
            if user_role != required_role:
                raise PermissionError(
                    f"{function.__name__} requires the {required_role!r} role"
                )
            return function(*args, **kwargs)

        return wrapper

    return decorator


def demonstrate_late_binding() -> list[Callable[[], int]]:
    """Show why a loop variable must be captured deliberately."""
    functions = []
    for number in range(3):
        functions.append(lambda number=number: number)
    return functions


def demonstrate_closures() -> None:
    """Run each example and print its result."""
    greeting = make_greeting("Anuj")
    print(greeting())

    first_counter = make_counter()
    second_counter = make_counter(10)
    print(f"First counter: {first_counter()}, {first_counter()}")
    print(f"Second counter: {second_counter()}, {second_counter()}")

    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"Double 5: {double(5)}")
    print(f"Triple 5: {triple(5)}")

    india_tax = make_tax_calculator(0.18)
    print(f"Price with tax: {india_tax(100):.2f}")

    @require_role("admin")
    def delete_record(record_id: int, *, user_role: str) -> str:
        return f"Deleted record {record_id}"

    print(delete_record(7, user_role="admin"))
    try:
        delete_record(7, user_role="viewer")
    except PermissionError as error:
        print(f"Permission denied: {error}")

    values = [function() for function in demonstrate_late_binding()]
    print(f"Captured loop values: {values}")

    # __closure__ exposes the captured cells for learning and debugging.
    print(
        "Greeting captured values:",
        tuple(cell.cell_contents for cell in greeting.__closure__ or ()),
    )


if __name__ == "__main__":
    demonstrate_closures()
# output - in this code we  see how closures work in python.
# Hello, Anuj!
# First counter: 1, 2
# Second counter: 11, 12
# Double 5: 10
# Triple 5: 15
# Price with tax: 118.00
# Deleted record 7
# Permission denied: delete_record requires the 'admin' role
# Captured loop values: [0, 1, 2]
# Greeting captured values: ('Anuj',)