import functools


def make_generator(f):
    def generator():
        count = 1
        while True:
            yield f(count)
            count += 1
    return generator


def fibonacci(n):
    if n <= 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def make_generator_mem(f):
    @functools.lru_cache(maxsize=None)
    def memoized_f(n):
        return f(n)
    return make_generator(memoized_f)


if __name__ == '__main__':
    fib_gen = make_generator(fibonacci)()
    print(next(fib_gen), end=' ')
    print(next(fib_gen), end=' ')
    print(next(fib_gen), end=' ')
    print(next(fib_gen), end=' ')
    for i in range(10):
        print(next(fib_gen), end=' ')

    print('\n')

    arith_seq_gen = make_generator(lambda n: 2 * n + 1)()
    print(next(arith_seq_gen), end=' ')
    print(next(arith_seq_gen), end=' ')
    print(next(arith_seq_gen), end=' ')
    for i in range(10):
        print(next(arith_seq_gen), end=' ')

    print('\n')

    geom_seq_gen = make_generator(lambda n: 2 ** n)()
    print(next(geom_seq_gen), end=' ')
    print(next(geom_seq_gen), end=' ')
    print(next(geom_seq_gen), end=' ')
    for i in range(10):
        print(next(geom_seq_gen), end=' ')

    print('\n')

    power_seq_gen = make_generator(lambda n: (n + 1) ** 2)()
    print(next(power_seq_gen), end=' ')
    print(next(power_seq_gen), end=' ')
    print(next(power_seq_gen), end=' ')
    for i in range(10):
        print(next(power_seq_gen), end=' ')

    print('\n')

    fib_gen_mem = make_generator_mem(fibonacci)()
    print(next(fib_gen_mem), end=' ')
    print(next(fib_gen_mem), end=' ')
    print(next(fib_gen_mem), end=' ')
    print(next(fib_gen_mem), end=' ')
    for i in range(10):
        print(next(fib_gen_mem), end=' ')
        