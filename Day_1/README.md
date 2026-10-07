# Python Identity, Equality, and Copying

This folder contains [`identity_demo.py`](./identity_demo.py), a small Python lesson about how variables refer to objects and how lists behave when they are assigned, copied, or modified.

The most important idea is:

> A variable in Python does not contain a list directly. It refers to a list object.

Understanding this distinction explains why changing one variable sometimes changes another variable as well.

## Topics covered

- Equality (`==`) versus identity (`is`)
- Assignment and aliasing
- Mutation versus reassignment
- Shallow copies
- Deep copies
- Why nested lists require special care

## Mutable and immutable objects

In simple words:

- **Mutable** means an object can be changed after it is created.
- **Immutable** means an object cannot be changed after it is created.

### Mutable example: list

A list is mutable because its items can be changed, added, or removed:

```python
numbers = [1, 2, 3]
numbers[0] = 100
numbers.append(4)

print(numbers)  # [100, 2, 3, 4]
```

The original list object was changed. No new list was required.

Other common mutable types are:

- `list`
- `dict`
- `set`

```python
person = {"name": "Anuj", "age": 20}
person["age"] = 21
print(person)  # {'name': 'Anuj', 'age': 21}

colors = {"red", "blue"}
colors.add("green")
print(colors)  # {'red', 'blue', 'green'} (order may vary)
```

### Immutable example: string

A string is immutable. Its characters cannot be changed directly:

```python
name = "anuj"

# This causes a TypeError:
# name[0] = "A"
```

To get a changed string, Python creates a new string:

```python
name = "anuj"
new_name = "A" + name[1:]

print(name)      # anuj
print(new_name)  # Anuj
```

The original string remains unchanged.

Other common immutable types are:

- `int`
- `float`
- `bool`
- `str`
- `tuple`
- `bytes`

```python
number = 10
number = number + 5
print(number)  # 15
```

The statement `number = number + 5` does not change the integer `10`. It creates the integer `15` and makes `number` refer to it.

### Mutable versus immutable comparison

| Type | Mutable? | Example |
|---|---:|---|
| `list` | Yes | `[1, 2, 3]` |
| `dict` | Yes | `{"name": "Anuj"}` |
| `set` | Yes | `{"red", "blue"}` |
| `int` | No | `10` |
| `float` | No | `3.14` |
| `str` | No | `"hello"` |
| `tuple` | No | `(1, 2, 3)` |
| `bool` | No | `True` |

### Why this matters with variables

When two variables refer to the same mutable object, a change through one variable is visible through the other:

```python
first = [1, 2, 3]
second = first

second.append(4)

print(first)   # [1, 2, 3, 4]
print(second)  # [1, 2, 3, 4]
```

This happens because both variables refer to the same list.

With an immutable object, an apparent change creates a new object instead:

```python
first = 10
second = first

second = second + 1

print(first)   # 10
print(second)  # 11
```

`first` remains `10` because integers cannot be changed in place.

### Important note about tuples

A tuple itself is immutable, so its items cannot be replaced:

```python
values = (1, 2, 3)

# This causes a TypeError:
# values[0] = 100
```

However, a tuple can contain a mutable object. That inner object can still change:

```python
values = ([1, 2], 3)
values[0].append(4)

print(values)  # ([1, 2, 4], 3)
```

The tuple structure did not change; the list inside the tuple changed.

## Running the example

From this directory, run:

```bash
python identity_demo.py
```

The script uses `print()` for the main demonstrations. Some lines such as `lst1` or `lst3, lst1` are written as expressions to show what would appear in an interactive Python shell or notebook; those expressions do not print anything when the file is run as a normal script.

## 1. Equality versus identity

Python provides two different questions:

### Equality: `==`

`==` compares values or contents.

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)  # True
```

Both lists contain the same values, so they are equal.

### Identity: `is`

`is` checks whether two variables refer to the exact same object.

```python
print(a is b)  # False
```

Although the lists have equal contents, they were created as two separate list objects.

### Quick comparison

| Expression | Question |
|---|---|
| `a == b` | Do `a` and `b` have equal values? |
| `a is b` | Are `a` and `b` the same object? |

Use `==` when comparing values. Use `is` mainly for object identity checks such as `value is None`. Do not use `is` as a replacement for `==` when comparing ordinary values.

## 2. Assignment creates an alias

When one list is assigned to another variable, Python does not create a new list:

```python
lst1 = [1, 2, 3, 4]
lst2 = lst1

print(lst1 is lst2)  # True
```

Both names point to the same list object. `lst2` is called an **alias** of `lst1`.

If the list is changed through either name, the shared object changes:

```python
lst2[1] = 1000

print(lst1)  # [1, 1000, 3, 4]
print(lst2)  # [1, 1000, 3, 4]
```

There is still only one list in memory. The two variables are simply two references to that list.

## 3. Mutation versus reassignment

These two operations are different.

### Mutation changes an existing object

Methods and item assignment can mutate a list:

```python
b = a
b.append(4)
b[0] = 100
```

Because `a` and `b` refer to the same list, both names observe the mutation.

### Reassignment points a variable at another object

Reassignment changes what a name refers to:

```python
a = [1, 2, 3]
b = a

b = [9, 8, 7]
```

After the last line, `b` refers to a new list. `a` still refers to `[1, 2, 3]`. Reassignment does not change the old list.

## 4. Shallow copy

A shallow copy creates a new outer list:

```python
lst3 = lst1.copy()
# Equivalent forms:
# lst3 = list(lst1)
# lst3 = lst1[:]
```

For a flat list, changing the copied list does not affect the original:

```python
lst1 = [1, 2, 3, 4]
lst3 = lst1.copy()

lst3[1] = 20

print(lst1)  # [1, 2, 3, 4]
print(lst3)  # [1, 20, 3, 4]
print(lst1 is lst3)  # False
```

The outer list objects are different.

## 5. Why shallow copies can still share nested objects

A shallow copy copies only the outer container. It does not recursively copy objects inside that container.

```python
nested_a = [[1, 2], [3, 4]]
nested_b = nested_a.copy()

nested_b[0][0] = 100

print(nested_a)  # [[100, 2], [3, 4]]
print(nested_b)  # [[100, 2], [3, 4]]
```

The outer lists are different, but their inner lists are shared:

```python
print(nested_a is nested_b)        # False
print(nested_a[0] is nested_b[0])  # True
```

Therefore:

- Changing an inner list affects both copies.
- Adding a completely new inner list to one outer list does not affect the other.

```python
nested_a.append([5, 6])

print(nested_a)  # [[100, 2], [3, 4], [5, 6]]
print(nested_b)  # [[100, 2], [3, 4]]
```

The `append()` operation changes only the outer list on which it is called.

## 6. Deep copy

A deep copy creates a new outer object and recursively copies the objects inside it.

```python
import copy

nested_a = [[1, 2], [3, 4]]
nested_b = copy.deepcopy(nested_a)

nested_b[0].append(99)

print(nested_a)  # [[1, 2], [3, 4]]
print(nested_b)  # [[1, 2, 99], [3, 4]]
```

The nested lists are separate too:

```python
print(nested_a is nested_b)        # False
print(nested_a[0] is nested_b[0])  # False
```

Use `copy.deepcopy()` when independent nested data is required and the objects involved support deep copying.

## 7. Copying behavior at a glance

| Operation | New outer list? | New nested lists? | Nested mutation shared? |
|---|---:|---:|---:|
| `b = a` | No | No | Yes |
| `b = a.copy()` | Yes | No | Yes |
| `b = list(a)` | Yes | No | Yes |
| `b = a[:]` | Yes | No | Yes |
| `b = copy.deepcopy(a)` | Yes | Yes, recursively | No |

## 8. Recommended mental model

Think of variables as labels attached to objects:

```text
a ─┐
   ├──> one shared list object
b ─┘
```

That is what happens after:

```python
b = a
```

After a shallow copy:

```text
a ───> outer list A ───> inner list X

b ───> outer list B ───> inner list X
```

The outer lists are separate, but the inner list is shared.

After a deep copy:

```text
a ───> outer list A ───> inner list X

b ───> outer list B ───> inner list Y
```

The complete structure is independent.

## 9. Common mistakes

### Mistake: expecting assignment to copy a list

```python
b = a
```

This creates an alias, not a copy. Use `a.copy()` or `copy.deepcopy(a)` depending on whether nested objects must be independent.

### Mistake: using `is` to compare values

```python
if a is b:
    ...
```

This checks identity, not content. Use `a == b` for value comparison.

### Mistake: assuming `.copy()` is always enough

`.copy()` is enough for a flat list when its elements are immutable values such as integers or strings. For nested mutable objects, use `copy.deepcopy()` when changes must not be shared.

### Mistake: forgetting that list methods mutate in place

Methods such as `append()`, `extend()`, `insert()`, `remove()`, `sort()`, and `reverse()` modify the existing list. If another variable refers to that list, it sees the change.

## 10. Practical rules

1. Use `==` to compare contents.
2. Use `is` for identity checks, especially `value is None`.
3. Remember that `b = a` creates another reference to the same object.
4. Use `.copy()` for an independent outer list.
5. Use `copy.deepcopy()` for an independent nested structure.
6. Check whether an operation mutates an object before sharing that object.
7. When debugging, compare both `a == b` and `a is b` to distinguish equal values from shared identity.

## Summary

The demo shows three levels of relationship:

- **Alias:** `b = a` — same object, so mutations are shared.
- **Shallow copy:** `b = a.copy()` — new outer object, but nested mutable objects may still be shared.
- **Deep copy:** `b = copy.deepcopy(a)` — independent nested structure.

Once the difference between an object and the names that refer to it is clear, the behavior of assignment, mutation, shallow copying, and deep copying becomes predictable.
