from read_log import read_log
from log_to_dict import log_to_dict
from nasa_log_utils import get_successful_requests


def print_dict_entry_dates(log_dict):
    for host, entries in log_dict.items():
        num_requests = len(entries)
        first_request = entries[0]['date']
        last_request = entries[-1]['date']
        num_successful_requests = get_successful_requests(entries)
        success_rate = num_successful_requests / num_requests if num_requests > 0 else 0

        print(f"Host: {host}")
        print(f"Number of requests: {num_requests}")
        print(f"First request date: {first_request}")
        print(f"Last request date: {last_request}")
        print(f"Success rate: {success_rate:.2%}")
        print()


if __name__ == "__main__":
    log_info_list = read_log()
    host_dict = log_to_dict(log_info_list)
    print_dict_entry_dates(host_dict)
