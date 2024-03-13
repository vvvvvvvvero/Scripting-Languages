def forall(pred, iterable):
    if len(iterable) == 0:
        return True
    elif pred(iterable[0]):
        return forall(pred, iterable[1:])
    else:
        return False


def exists(pred, iterable):
    if len(iterable) == 0:
        return False
    elif pred(iterable[0]):
        return True
    else:
        return exists(pred, iterable[1:])


def at_least(n, pred, iterable):
    if n == 0:
        return True
    elif len(iterable) == 0:
        return False
    elif pred(iterable[0]):
        return at_least(n - 1, pred, iterable[1:])
    else:
        return at_least(n, pred, iterable[1:])


def at_most(n, pred, iterable):
    if n < 0:
        return False
    elif len(iterable) == 0:
        return True
    elif pred(iterable[0]):
        return at_most(n - 1, pred, iterable[1:])
    else:
        return at_most(n, pred, iterable[1:])


if __name__ == '__main__':
    print('forall')
    print(forall(lambda x: x % 2 == 0, [-2, 4, 6, 8, 10]))
    print(forall(lambda x: x % 2 == 0, [2, 4, 6, 7, 10]))
    print(forall(lambda word: len(word) == 5, ('kasia', 'miała', 'kotów')))
    print('exists')
    print(exists(lambda obj: isinstance(obj, list), [1, ['a', 'b'], 3, (1, 2), 'c']))
    print(exists(lambda x: x % 2 == 0, [-3, 5, 7, 9, 1]))
    print(exists(lambda t: len(t) == 0, ((1, 2), (1, 2, 3), ())))
    print('at_least')
    print(at_least(6, lambda x: x % 2 == 0, [-2, 4, 6, 8, 10]))
    print(at_least(3, lambda x: x % 2 == 0, [-2, 4, 3, 7, 10, 8]))
    print(at_least(2, lambda word: len(word) == 5, ('kasia', 'ma', 'kota')))
    print('at_most')
    print(at_most(2, lambda x: x % 2 == 0, [-2, 3, 6, 9, 11]))
    print(at_most(3, lambda x: x % 2 == 0, [-2, 4, 3, 7, 10, 8]))
    print(at_most(1, lambda obj: isinstance(obj, tuple), [1, ['a', 'b'], 3, (1, 2), 'c']))
