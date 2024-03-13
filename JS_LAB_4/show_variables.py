from os import environ
import sys


def filter_args(env_args):
    filtered_args = {}
    for name in env_args:
        if name in list(environ.keys()) and name not in filtered_args:
            filtered_args[name] = environ[name]
    return filtered_args


def show_environment_vars():
    if len(sys.argv) > 1:
        var_names = filter_args(sys.argv[1:])
        for elem in sorted(var_names):
            print(f"{elem} = {var_names[elem]}")
    else:
        for elem in sorted(environ):
            print(f"{elem} = {environ[elem]}")


if __name__ == '__main__':
    show_environment_vars()
