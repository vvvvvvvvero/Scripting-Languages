from read_log import read_log


def print_entries(entries):
    for entry in entries:
        host, date, path, code, size = entry
        print(f"{host:<40} {date:%d/%b/%Y:%H:%M:%S\t} {path:<60} {code:<5} {size:<10}")


if __name__ == "__main__":
    log_info_list = read_log()
    print_entries(log_info_list)
