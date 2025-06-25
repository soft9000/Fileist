'''
Generative:

We need a program that will show us a short list of
files that have been changed on our computer. We would
like to have the program find the newest, and oldest
for us. Being able to locate files of a certain type
is also important.
'''
import os
import argparse
from datetime import datetime

def find_files(base_dir, file_ext=None):
    files_with_times = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file_ext and not file.lower().endswith(file_ext.lower()):
                continue
            full_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(full_path)
                files_with_times.append((full_path, mtime))
            except Exception:
                continue  # skip files that can't be accessed
    return files_with_times

def print_results(files_with_times, count=5):
    if not files_with_times:
        print("No files found.")
        return
    files_sorted = sorted(files_with_times, key=lambda x: x[1])
    print(f"\nOldest {min(count, len(files_sorted))} files:")
    for path, mtime in files_sorted[:count]:
        print(f"{datetime.fromtimestamp(mtime)} - {path}")

    print(f"\nNewest {min(count, len(files_sorted))} files:")
    for path, mtime in reversed(files_sorted[-count:]):
        print(f"{datetime.fromtimestamp(mtime)} - {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find oldest and newest changed files.")
    parser.add_argument("directory", help="Directory to search")
    parser.add_argument("--ext", help="File extension to filter by (e.g. .txt, .py)", default=None)
    parser.add_argument("--count", help="Number of oldest/newest files to show", type=int, default=5)
    args = parser.parse_args()

    files = find_files(args.directory, args.ext)
    print_results(files, args.count)
