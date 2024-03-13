from read_log import read_log
from print_log import print_entries


def get_failed_reads(log_list, to_merge):
    code4xx_list = []
    code5xx_list = []
    for entry in log_list:
        if 400 <= entry[-2] < 500:
            code4xx_list.append(entry)
        elif 500 <= entry[-2] < 600:
            code5xx_list.append(entry)

    if to_merge:
        return code4xx_list + code5xx_list
    else:
        return code4xx_list, code5xx_list


if __name__ == "__main__":
    log_info_list = read_log()
    failed = get_failed_reads(log_info_list, True)
    print_entries(failed)

