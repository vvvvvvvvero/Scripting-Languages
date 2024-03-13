from utils import parse_ssh_log


def log_to_list(filename: str) -> list:
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    return lines


def log_list_to_dict_list(filename: str) -> list:
    log_list = log_to_list(filename)
    return [parse_ssh_log(line) for line in log_list]


def get_log_dict_list() -> list:
    return log_list_to_dict_list('/Users/veraemelianova/Desktop/SSH.log')


def get_log_list() -> list:
    return log_to_list('/Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log')


def print_log_dict_list() -> None:
    for log in get_log_dict_list():
        print(log)


if __name__ == '__main__':
    print_log_dict_list()
