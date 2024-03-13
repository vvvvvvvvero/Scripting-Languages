from read_log import read_log


def get_entries_by_addr(log_list, host_name):
    filtered_entries = []
    for entry in log_list:
        if entry[0] == host_name:
            filtered_entries.append(entry)
    return filtered_entries


if __name__ == "__main__":
    log_info_list = read_log()
    print(get_entries_by_addr(log_info_list, "titan02f"))
