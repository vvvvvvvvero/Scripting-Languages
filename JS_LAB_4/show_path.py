import os
from os import environ
import argparse

dir_list = environ['PATH'].split(os.pathsep)


def print_path_dirs():
    for d in dir_list:
        print(d)


def print_exec_files():
    for d in dir_list:
        print(f"\n{d}:")
        for file_name in os.listdir(d):
            file_path = os.path.join(d, file_name)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                print(f"{file_name}")


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dirs', action='store_true', help='Print all directories in the PATH variable')
parser.add_argument('-e', '--exec', action='store_true',
                    help='Print each directory in the PATH variable and all executables')
args = parser.parse_args()


if __name__ == '__main__':
    if args.dirs:
        print_path_dirs()
    elif args.exec:
        print_exec_files()
    else:
        parser.print_help()
