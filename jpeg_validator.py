import os
import time
from PIL import Image
import exifread
import concurrent.futures

folder_path = '/path/to/photo/library'

def process_file(file_path):
    with open('file_error.txt', 'a') as error_log:
        try:
            with open(file_path, 'rb') as f:
                Image.open(f).verify()
            
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, strict=True)
        
        except (IOError, SyntaxError) as e:
            error_log.write(f'{time.asctime()}: {file_path} could not be opened - {e}\n')
        
        except (AttributeError, KeyError, IndexError) as e:
            error_log.write(f'{time.asctime()}: {file_path} has invalid metadata - {e}\n')

# Get list of all JPEG files in the folder
jpeg_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.jpeg')]

# Set maximum number of threads to use
num_threads = 4

# Process files in parallel using threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(process_file, f) for f in jpeg_files]

    # Wait for all threads to finish
    for future in concurrent.futures.as_completed(futures):
        pass
