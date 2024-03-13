import string
import random


class PasswordGenerator:
    def __init__(self, length, charset, count):
        self.length = length
        self.charset = charset if charset else list(string.ascii_letters + string.digits)
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0:
            raise StopIteration
        self.count -= 1
        return ''.join([random.choice(self.charset) for _ in range(self.length)])


if __name__ == '__main__':
    pg_default = PasswordGenerator(10, None, 6)
    print(next(pg_default))
    print(next(pg_default))
    for password in pg_default:
        print(password)

    pg_custom = PasswordGenerator(5, ['?', '#', '!', '+', '-', 'a', 'b', 'c', 'd'], 3)
    print(next(pg_custom))
    print(next(pg_custom))
    print(next(pg_custom))
    print(next(pg_custom))

