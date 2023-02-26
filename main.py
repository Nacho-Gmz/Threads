from threading import Thread
from threading import Lock
from setup import create_files, delete_files, get_file_names
import time

def process_file(file_path, lock):
    with open(file_path, 'r') as f:
        # read the contents of the file
        contents = f.read()
        
        # count the number of lines in the file
        num_lines = len(contents.split('\n'))
       
        # print the result
        with lock:
            print(f"Processed {file_path}: {num_lines} lines")

def process_files(files):
    threads = []
    for file in files:
        t = Thread(target=process_file, args=(file, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# creates 100 files with random newline characters in them
create_files()

# gets a list of all the filenames and the path to each one
files_to_process = get_file_names()

# shared lock
lock = Lock()

start_time = time.time()

# sends the file names and paths to the thread creating function
process_files(files_to_process)

end_time = time.time()

print(f"Finished processing all files in {end_time - start_time:.2f} seconds")

#deletes the files once the program finishes
delete_files()