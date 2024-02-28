# unzip zip files using multi-thread and Multiprocessing. Note this op is not thread-safe.

import zipfile
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import argparse 
from glob import glob 
import os.path as osp
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description="Unzip zip files using multi-thread")
    parser.add_argument('--data_root', type=str, default='path/to/your/*.zip', help='path to the zip files')
    parser.add_argument('--extract_path', type=str, default='path/to/extract', help='path to extract the zip files')
    parser.add_argument('--num_threads', type=int, default=4, help='number of threads to use')
    parser.add_argument('--num_processes', type=int, default=16, help='number of processes to use')
    args = parser.parse_args()
    return args

def unzip_file(zip_file, extract_path):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_path)


def multi_thread_unzip(zip_file, extract_path, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor
        futures = [executor.submit(unzip_file, zip_file, extract_path) for _ in range(num_threads)]

        # Wait for all tasks to complete
        for future in tqdm(futures, total=len(futures)):
            future.result()

def multi_thread_and_process_unzip(zip_files, extract_path, num_threads, num_processes):
    with ProcessPoolExecutor(max_workers=num_processes) as process_executor:
        # Multiprocessing: Submit tasks to the process executor
        process_futures = [process_executor.submit(multi_thread_unzip, zip_file, extract_path, num_threads) for zip_file in zip_files]

        # Wait for all multiprocessing tasks to complete
        for future in process_futures:
            future.result()

def main():
    args = parse_args()
    zip_files = glob(osp.join(args.data_root, '*.zip'))
    multi_thread_and_process_unzip(zip_files, args.extract_path, args.num_threads, args.num_processes)

if __name__ == '__main__':
    main()
