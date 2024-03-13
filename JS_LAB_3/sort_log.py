from read_log import read_log


def sort_log(log_list, index):
    try:
        sorted_logs = sorted(log_list, key=lambda entry: entry[index])
    except IndexError:
        print("Invalid sort key index")
        return log_list
    else:
        return sorted_logs


if __name__ == "__main__":
    log_info_list = read_log()
    print(sort_log(log_info_list, 3))