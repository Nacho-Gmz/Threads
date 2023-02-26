import random
import os

def create_files():
    for i in range(1, 101):
        filename = f"files/file_{i}.txt"
        with open(filename, "w") as f:
            num_newlines = random.randint(1, 100)
            f.write("\n" * num_newlines)

def delete_files():
    for i in range(1, 101):
        filename = f"files/file_{i}.txt"
        if os.path.exists(filename):
            os.remove(filename)

def get_file_names():
    file_names = []
    for i in range(1, 101):
        filename = f"files/file_{i}.txt"
        if os.path.exists(filename):
            file_names.append(filename)
    return file_names
