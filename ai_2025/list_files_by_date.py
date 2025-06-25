'''
Generative:

Use Python to create an argparse program to display a
date-sorted list of files. 

The program is to have a ‘Progress Display’ followed
by a ‘Reporting Display.’

The Reporting Display:

After the detection process list each file in descending
order based upon any files’ last modification time. The
final file list display begins with number 1.

The File Detection Progress Display:

Print a single ‘+’ whenever adding or replacing any file
to the final list, print a single ‘.’ when the file is
not to be added to the report, else print a single ‘!’
whenever a file cannot be accessed. 

No newlines should be printed during the file detection
process but be sure to print a newline both before and
after all file detections.

Command-Line Options:

Optional command-line options can be used to:

(1)	Support an optional ‘list’ option. If specified,
this ‘list’ parameter is used to define the number of files
to list onto the command line interface. The default number
of files to ‘list’ is 25.

(2)	Support an optional ‘suffix’ option. If specified,
this ‘suffix’ option is used to detect file names matching
an arbitrary string suffix. The default file suffix is an
empty string.

(3)	Support an optional ‘oldest’ option. If specified,
this ‘oldest’ option is used to invert the search so as to
detect a set of the oldest, rather than the default newest,
files.

'''
import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Display a date-sorted list of files with progress and report displays."
    )
    parser.add_argument(
        "--list", type=int, default=25, help="Number of files to list (default: 25)"
    )
    parser.add_argument(
        "--suffix", type=str, default="", help="File suffix to match (default: '')"
    )
    parser.add_argument(
        "--oldest", action="store_true", help="Show oldest files instead of newest"
    )
    parser.add_argument(
        "path", nargs="?", default=".", help="Directory to scan (default: current directory)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    files = []
    suffix = args.suffix
    target_dir = args.path

    # Start progress display
    print()  # Print a newline before progress
    sys.stdout.flush()

    # Walk the directory tree
    for root, dirs, filenames in os.walk(target_dir):
        for fname in filenames:
            fpath = os.path.join(root, fname)
            try:
                if not os.path.isfile(fpath):
                    print('.', end='', flush=True)
                    continue
                if suffix and not fname.endswith(suffix):
                    print('.', end='', flush=True)
                    continue
                try:
                    mtime = os.path.getmtime(fpath)
                except Exception:
                    print('!', end='', flush=True)
                    continue

                files.append((fpath, mtime))
                print('+', end='', flush=True)
            except Exception:
                print('!', end='', flush=True)

    print()  # Newline after progress

    # Sort files
    files.sort(key=lambda x: x[1], reverse=not args.oldest)

    # Reporting display
    print("\nReporting Display:")
    to_list = files[:args.list]
    for idx, (fpath, mtime) in enumerate(to_list, start=1):
        print(f"{idx}. {fpath}")

if __name__ == "__main__":
    main()
