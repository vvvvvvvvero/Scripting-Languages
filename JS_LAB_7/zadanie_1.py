from collections.abc import Iterable


def acronym(world_list: list) -> str:
    return ''.join(map(lambda word: word[0], world_list))


def median(num_list: list) -> float:
    sorted_numbers = sorted(num_list)
    length = len(num_list)
    middle = length // 2
    if length % 2 == 0:
        return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2
    else:
        return sorted_numbers[middle]


def root(num, epsilon):
    if num < 0:
        print('Nie można obliczyć pierwiastka z liczby ujemnej')
        return None
    if epsilon < 0:
        print('Epsilon nie może być mniejszy od zera')
        return None
    return root_helper(num, epsilon, num / 2)


def root_helper(num, epsilon, approx):
    if abs(approx ** 2 - num) < epsilon:
        return approx
    else:
        return root_helper(num, epsilon, (approx + num / approx) / 2)


def make_alfa_dict(line: str):
    words = line.split()
    alpha_dict = {}

    def process_word(word):
        def process_char(char):
            if char.isalpha():
                if char not in alpha_dict:
                    alpha_dict[char] = []
                if word not in alpha_dict[char]:
                    alpha_dict[char].append(word)
        list(map(lambda ch: process_char(ch), list(filter(lambda char: char.isalpha(), word))))
    list(map(lambda word: process_word(word), words))
    return alpha_dict


def flatten(list_of_lists: list) -> list:
    if len(list_of_lists) == 0:
        return []
    if isinstance(list_of_lists[0], Iterable) and not isinstance(list_of_lists[0], str):
        return flatten(list(list_of_lists[0])) + flatten(list_of_lists[1:])
    else:
        return [list_of_lists[0]] + flatten(list_of_lists[1:])

# list(elem) -> dla iterables
# [elem] -> dla nie iterables


if __name__ == '__main__':
    print(acronym(['Zakład', 'Ubezpieczeń', 'Społecznych', 'w', 'Polsce']))
    print(acronym(['Unia', 'Europejska']))

    print(median([3, 5, 2, -9, 20, 6, -3]))
    print(median([1]))
    print(median([2, 1]))
    print(median([]))

    print(root(3, epsilon=0.1))
    print(root(625, epsilon=0.000001))
    print(root(-9, epsilon=0.001))

    print(make_alfa_dict('on i ona'))
    print(make_alfa_dict('ala ma kota i psa'))
    print(make_alfa_dict('Ab cD eFa bC dE'))

    print(flatten([1, 2, 3, [4, 5, [6, 7, 8], 9], 10, [11, 12]]))
    print(flatten([1, 10, ["hello", "python", [(1, "wow"), (2, "cool")]], "world", 3]))

