from read_log import read_log


def get_entries_by_code(log_list, http_code):
    filtered_entries = []
    for entry in log_list:
        if entry[-2] == http_code:
            filtered_entries.append(entry)
    return filtered_entries


if __name__ == "__main__":
    log_info_list = read_log()
    print(get_entries_by_code(log_info_list, 501))

