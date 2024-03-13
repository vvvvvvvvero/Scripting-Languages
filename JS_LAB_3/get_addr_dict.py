from read_log import read_log
from log_to_dict import log_to_dict


def get_addr(log_dict):
    key_list = list(log_dict.keys())
    return key_list


if __name__ == "__main__":
    log_info_list = read_log()
    host_dict = log_to_dict(log_info_list)
    print(get_addr(host_dict))

