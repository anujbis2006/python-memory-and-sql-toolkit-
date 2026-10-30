# Code	Explanation
# import gc	Garbage collector module import
# class Node	Custom object create karne ke liye class
# a = Node()	First object
# b = Node()	Second object
# a.other = b	First object references second
# b.other = a	Second object references first
# del a	External reference delete
# del b	Second external reference delete
# gc.collect()	Cyclic garbage collection trigger
import gc
class Node:
    pass
def create_reference_cycle():
    a = Node()
    b = Node()
    a.other = b
    b.other = a

    print("Reference cycle created")
    del a
    del b
    print("External references deleted")
    collected = gc.collect()
    print("Objects collected:", collected)
create_reference_cycle()


# ____________________________//____________________________
# Line-by-line explanation:
# 1. import tracemalloc: Import memory profiling module.
# 2. tracemalloc.start(): Start tracking allocations.
# 3. before: Capture memory state before creating list.
# 4. data = [...]: Create a list containing 100,000 integers.
# 5. after: Capture memory state after list creation.
# 6. compare_to(): Compare both snapshots.
# 7. statistics[:5]: Show five biggest allocation differences.
# 8. get_traced_memory(): Get current and peak traced memory.
# 9. stop(): Stop tracking.
# Experiment: Change 100000 to 1000000 and then 10000000.

# Observe how memory consumption changes.

# Don't assume the memory will increase in an exactly linear manner because Python allocation overhead and allocator behaviour also matter.
import tracemalloc
# tracemalloc before and after a list build
tracemalloc.start()
before = tracemalloc.take_snapshot()
data = [i for i in range(100000)]
after = tracemalloc.take_snapshot()
print("Memory comparison:")
stats = after.compare_to(before, "lineno")
for stat in stats[:5]:
    print(stat)
current, peak = tracemalloc.get_traced_memory()
print("Current memory:", current)
print("Peak memory:", peak)
tracemalloc.stop()

# BUILD: Create your own Memory & Time Profiler

import gc
import sys
import time
import tracemalloc
from functools import wraps


# --------------------------------
# 1. REFERENCE COUNTING
# --------------------------------

def reference_count_demo():
    data = [10, 20, 30]
    print("\n--- REFERENCE COUNTING ---")
    print("Initial:", sys.getrefcount(data))
    another = data
    print("After another reference:", sys.getrefcount(data))
    del another
    print("After deleting reference:", sys.getrefcount(data))


# --------------------------------
# 4. CUSTOM MEMORY + TIME DECORATOR
# --------------------------------

def profile_memory_and_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        already_tracing = tracemalloc.is_tracing()
        if not already_tracing:
            tracemalloc.start()
        tracemalloc.reset_peak()
        before_memory, _ = tracemalloc.get_traced_memory()
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            after_memory, peak_memory = tracemalloc.get_traced_memory()
            print(f"\nFunction: {func.__name__}")
            print(f"Execution time: {end_time - start_time:.6f} seconds")
            print(f"Current memory change: {after_memory - before_memory} bytes")
            print(f"Peak traced memory: {peak_memory} bytes")
            if not already_tracing:
                tracemalloc.stop()

        return result
    return wrapper


# --------------------------------
# 5. TEST THE CUSTOM DECORATOR
# --------------------------------

@profile_memory_and_time
def create_large_list():
    numbers = [i for i in range(100000)]
    return numbers


# --------------------------------
# 6. MAIN
# --------------------------------

if __name__ == "__main__":
    reference_count_demo()
    create_reference_cycle()
    print("\n--- CUSTOM PROFILER ---")
    result = create_large_list()
    print("List length:", len(result))