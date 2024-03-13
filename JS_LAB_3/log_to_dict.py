from read_log import read_log
from entry_to_dict import entry_to_dict


def log_to_dict(entries):
    dictionary_by_host = {}
    for entry in entries:
        host = entry[0]
        dict_entry = entry_to_dict(entry)
        if host in dictionary_by_host:
            dictionary_by_host[host].append(dict_entry)
        else:
            dictionary_by_host[host] = [dict_entry]
    return dictionary_by_host


if __name__ == "__main__":
    log_info_list = read_log()
    host_dict = log_to_dict(log_info_list)
    print(host_dict['midcom.com'])
