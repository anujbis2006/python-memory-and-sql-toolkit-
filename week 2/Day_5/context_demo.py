# Context Manager Demo

# its helps to manage resources like file handling, 
# network connections, and database connections. 
# Context managers ensure that resources are properly acquired and released, 
# even in the presence of exceptions.

from contextlib import contextmanager
# this module provides a way to create context 
# managers using a simple function-based syntax.

# and now we can use by decorator @contextmanager 
# to create a context manager function.

class open_File():
#  This is a context manager class that opens a file 
# and ensures that it is properly closed after use.
    def __init__(self,filename,mode):
        self.filename = filename
        self.mode = mode

# The __enter__ method is called when the execution flow 
# enters the context of the with statement.
    def __enter__(self):
        self.file = open(self.filename,self.mode)
        return self.file

# this __exit__ method is called when the execution
#  flow exits the context of the with statement.

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

with open_File('test.txt','w') as f:
    f.write('Hello, World!')

# The overall code tells that the file is opened in write mode, 
# and the string "Hello, World!" is written to it.


print(f.closed)
 # True - if this tells true then the file is
# closed after the with block is executed.


@contextmanager
def open_file(filename,mode):

# in this Code snippet, we define a context manager function called 
# open_file that takes a filename and mode as arguments.
    try:
        f = open(filename,mode)
        yield f
    finally:
        f.close()



with open_file('simple.txt','w') as f:
    f.write('Hello, World!')

print(f.closed) # True - if this tells true then the file is closed after the 
# with block is executed.


import os 
from contextlib import contextmanager

cwd  = os.getcwd() # get the current working directory
os.chdir('Sample-Dir-One') # change the current working directory to the parent directory
print(os.listdir()) # list the files and directories in the current working directory
os.chdir(cwd) # change the current working directory back to the original directory

cwd = os.getcwd() # get the current working directory
os.chdir('Sample-Dir-Two') # change the current working directory to the parent directory
print(cwd) # print the current working directory
os.chdir(cwd) # change the current working directory back to the original directory

# output ['mydoc.txt', 'myfile.txt', 'myfolder'] - this is the list of files and directories in the current working directory


@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd() # get the current working directory
        os.chdir(destination) # change the current working directory to the parent directory
        yield # now we are done with the context manager, we can yield control back to the caller
    finally:
        os.chdir(cwd) # change the current working directory back to the original directory

with change_dir('Sample-Dir-Two'):
    print(os.listdir()) # list the files and directories in the current working directory

# output ['mydoc.txt', 'myfile.txt', 'myfolder'] - this gives the same is the list of files and directories in the current working directory


# using context manger by using __exit__ and __enter__ methods
class File:
    def __init__(self, name:str):
        self.name = name

    def __enter__(self):
        print(f'Opening file: {self.name}....')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'Closing file: {self.name}....')

if __name__ == '__main__':
    with File('test.txt') as f:
        print(f'Working with file: {f.name}....')

    print('Done!') 