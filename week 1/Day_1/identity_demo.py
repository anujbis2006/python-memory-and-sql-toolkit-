# # Difference between identity and equality
# a = [1, 2, 3]
# b = [1, 2, 3]
# print(a == b)  # True, because the contents are equal
# print(a is b)  # False, because they are different objects in memory

# b.append(4)
# print(a == b)  # False, because the contents are now different


# =,Deepcopy and Shallow copy/copy
lst1 = [1, 2, 3,4]
lst2 = lst1  # This creates a reference to the same list object
print(lst1 is lst2)  # True, because both variables point to the same object

lst2[1] = 1000
lst2 # [1, 1000, 3, 4]  # The change is reflected in lst1 as well

lst1 # [1, 1000, 3, 4]  # lst1 is also affected because lst2 is just a reference to lst1
# beacuse it allocated to the same memory location

# shallow copy
import copy
lst3 = lst1.copy() # This creates a shallow copy of lst1\
lst3[1] = 20
lst3,lst1 # ([1, 20, 3, 4], [1, 1000, 3, 4])  # lst1 remains unchanged
# beacuse lst3 is a new object in memory, separate from lst1

# shallow copy nested list
nst_lst1 = [[1, 2], [3, 4]]
nst_lst2 = nst_lst1.copy()  # This creates a shallow copy of nst_lst1
nst_lst1[1][0] = 100
nst_lst1 # [[1, 2], [100, 4]]  # The change is reflected in nst_lst2 as well
nst_lst2 # [[1, 2], [100, 4]]  # Because the inner lists are still references to the same objects in memory

nst_lst1.append([2,3,4,5])
nst_lst1 # [[1, 2], [100, 4], [2, 3, 4, 5]]  # The new inner list is added to nst_lst1
nst_lst2 # [[1, 2], [100, 4]]  # nst_lst2 remains unchanged because it is a separate list object, but the inner lists are still shared

# deep copy
deep_lst1 = [1,2,3,4]
deep_lst2 = copy.deepcopy(deep_lst1)  # This creates a deep copy of deep_lst1
deep_lst2[1] = 2000
deep_lst2 # [1, 2000, 3, 4]  # The change is reflected only in deep_lst2
deep_lst1 # [1, 2, 3, 4]  # deep_lst1 remains unchanged because deep_lst2 is a completely separate object in memory

# nested deep copy
nst_deep_lst1 = [[1, 2], [3, 4]]
nst_deep_lst2 = copy.deepcopy(nst_deep_lst1)  # This creates a deep copy of nst_deep_lst1
nst_deep_lst2[1][0] = 100
nst_deep_lst2 # [[1, 2], [100, 4]]  # The change is reflected only in nst_deep_lst2
nst_deep_lst1 # [[1, 2], [3, 4]]



# homework assignment
# basic identity
a = [1, 2, 3]
b = a
print(a == b)
# True, because the contents are equal
print(a is b)
# True, because they are the same object in memory

# separate list
a = [1,2,3,4]
b = [1,2,3,4]
print(a == b)
# True, because the contents are equal
print(a is b)
# False, because they are different objects in memory


# aliasing
a = [1, 2, 3]
b = a  # b is an alias for a
b.append(4)
print(a) #[1,2,3,4] # The change is reflected in a as well


# shallow copy
a = [1, 2, 3]
b = a.copy()
b.append(4)
print(a) #[1,2,3] # a remains unchanged because b is a separate object in memory
# print(b) #[1,2,3,4] has different memory location than a

# nested shallow copy
a = [[1, 2], [3, 4]]
b = a.copy()  # This creates a shallow copy of a
b[0][0] = 100
print(a) #[[100, 2], [3, 4]] # The change is reflected in a as well because the inner lists are still references to the same objects in memory
print(b) #[[100, 2], [3, 4]] # b is a separate list object, but the inner lists are still shared

# deep copy nested list
import copy
a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0].append(99)
print(a) # [[1, 2], [3, 4]] # a remains unchanged because b is a completely separate object in memory
print(b)# [[1, 2, 99], [3, 4]] # b is a separate list object with its own inner lists

# reassignment vs mutation
a = [1, 2, 3]
b = a  # b is an alias for a
b.append(4)  # This mutates the list that both a and b refer to
print(a) #[1, 2, 3, 4] # The change is reflected in both a and b
print(b) #[1, 2, 3, 4] # The change is reflected in both a and b


# id() function
a = [1, 2, 3]
print(id(a)) # prints the memory address of a
# 43456789876


# mutable and immutable
#
# Mutable means an object can be changed after it is created.
# Common mutable types: list, set, dictionary, and bytearray.


mutable_numbers = [1, 2, 3]
mutable_numbers[0] = 100
mutable_numbers.append(4)
print(mutable_numbers)  # [100, 2, 3, 4]

mutable_person = {"name": "Anuj", "age": 20}
mutable_person["age"] = 21
print(mutable_person)  # {'name': 'Anuj', 'age': 21}

# Two variables can refer to the same mutable object.
first_list = [1, 2, 3]
second_list = first_list
second_list.append(4)
print(first_list)   # [1, 2, 3, 4]
print(second_list)  # [1, 2, 3, 4]

# Immutable means an object cannot be changed after it is created.
# Common immutable types: int, float, bool, string, tuple, and bytes.

number = 10
number = number + 5
print(number)  # 15; a new integer object is used

text = "python"
# text[0] = "P"  # TypeError: strings cannot be changed directly
new_text = "P" + text[1:]
print(text)      # python
print(new_text)  # Python

# Reassigning an immutable value does not change another variable.
first_number = 10
second_number = first_number
second_number = second_number + 1
print(first_number)   # 10
print(second_number)  # 11

# A tuple is immutable, but it can contain a mutable list.
tuple_with_list = ([1, 2], 3)
tuple_with_list[0].append(4)
print(tuple_with_list)  # ([1, 2, 4], 3)
