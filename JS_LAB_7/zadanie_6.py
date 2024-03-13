import logging
import time
import functools
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(levelname)s  %(message)s', stream=sys.stdout)


def log(level):
    def decorator(func_or_class):
        if isinstance(func_or_class, type):
            return log_class(level, func_or_class)
        else:
            return log_function(level, func_or_class)
    return decorator


def log_function(level, func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.log(level, f'Calling {func.__name__} with arguments: {args} and keyword arguments: {kwargs}')
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logging.log(level, f'Finished {func.__name__} with result {result} in {(end - start):.10f} seconds')
        return result
    return wrapper


def log_class(level, cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        logging.log(level, f'Creating instance of class point {cls.__name__} with arguments: {args} and keyword arguments: {kwargs}')
        instance = cls(*args, **kwargs)
        logging.log(level, f'Finished {cls.__name__} with result {instance}')
        return instance
    return wrapper


@log(logging.WARNING)
def file_statistics(file_path, mode):
    with open(file_path, mode) as f:
        lines = f.readlines()
    return {
        'Lines': len(lines),
        'Words': sum([len(line.split()) for line in lines]),
        'Characters': sum([len(line) for line in lines])
    }


@log(logging.CRITICAL)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'Point({self.x}, {self.y})'


if __name__ == '__main__':
    print(file_statistics('zadanie_6.py', mode='r'))
    print(Point(1, 2))
