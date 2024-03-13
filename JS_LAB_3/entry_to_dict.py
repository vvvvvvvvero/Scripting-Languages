from datetime import datetime
from read_log import read_log


def entry_to_dict(entry):
    host, date, path, code, size = entry
    date_str = datetime.strftime(date, '%Y-%m-%d:%H:%M:%S')

    entry_dict = {
        'host': host,
        'date': date_str,
        'path': path,
        'code': code,
        'size': size,
    }

    return entry_dict


if __name__ == "__main__":
    log_info_list = read_log()
    print(entry_to_dict(log_info_list[0]))
