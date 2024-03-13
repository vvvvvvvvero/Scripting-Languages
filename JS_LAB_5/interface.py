import argparse
from extract_info import *
from process_ssh_log import *
from log_statistics import get_n_random_user_logs, get_most_and_least_frequent_user,\
    get_average_time_global, get_average_time_for_user

parser = argparse.ArgumentParser("CLI")
parser.add_argument("log_file", help="Path to log file")
parser.add_argument("-l", "--log_level", choices=["debug", "info", "warning", "error", "critical"])


def list_logs():
    logs = log_to_list(args.log_file)
    for i, l in enumerate(logs):
        print(f'{i}. {l}')
# python3 interface.py /Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log list-logs


def parse_log():
    logs = log_to_list(args.log_file)
    index = int(args.line_num)
    if index < 0 or index >= len(logs):
        print("Invalid index")
    else:
        print(parse_ssh_log(logs[index]))
# python3 interface.py /Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log parse-log -l 1


def ip_address():
    logs = log_to_list(args.log_file)
    index = int(args.line_num)
    if index < 0 or index >= len(logs):
        print("Invalid index")
    else:
        print(get_ipv4s_from_log(parse_ssh_log(logs[index])))
# python3 interface.py /Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log ip-address -l 1


def user():
    logs = log_to_list(args.log_file)
    index = int(args.line_num)
    if index < 0 or index >= len(logs):
        print("Invalid index")
    else:
        print(get_user_from_log(parse_ssh_log(logs[index])))
# python3 interface.py /Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log user -l 2


def message():
    logs = log_to_list(args.log_file)
    index = int(args.line_num)
    if index < 0 or index >= len(logs):
        print("Invalid index")
    else:
        print(get_message_type_from_log(parse_ssh_log(logs[index])))
# python3 interface.py /Users/veraemelianova/PycharmProjects/JS_LAB_5/SSH_short.log user -l 2


def random_logs():
    logs = log_list_to_dict_list(args.log_file)
    rand_logs = get_n_random_user_logs(logs, int(args.number))
    for rand_log in rand_logs:
        print(rand_log)
# python3 interface.py SSH_short.log random-logs -n 2


def frequency():
    logs = log_list_to_dict_list(args.log_file)
    print(get_most_and_least_frequent_user(logs))
# python3 interface.py SSH_short.log frequency


def global_statistics():
    logs = log_list_to_dict_list(args.log_file)
    print(get_average_time_global(logs))
# python3 interface.py /Users/veraemelianova/Desktop/SSH.log global-stats


def user_statistics():
    logs = log_list_to_dict_list(args.log_file)
    print(get_average_time_for_user(logs, args.user))
# python3 interface.py /Users/veraemelianova/Desktop/SSH.log user-stats -u "fztu"


subparsers = parser.add_subparsers(title='Subparsers', help="Command to execute")

list_all_logs_parsers = subparsers.add_parser("list-logs", help="List all logs")
list_all_logs_parsers.set_defaults(func=list_logs)

log_parser = subparsers.add_parser("parse-log", help="Parse log file")
log_parser.add_argument("-l", "--line_num", help="Number of line to parse")
log_parser.set_defaults(func=parse_log)

ip_parser = subparsers.add_parser("ip-address", help="Get IP address")
ip_parser.add_argument("-l", "--line_num", help="Number of line to parse")
ip_parser.set_defaults(func=ip_address)

user_parser = subparsers.add_parser("user", help="Get user")
user_parser.add_argument("-l", "--line_num", help="Number of line to parse")
user_parser.set_defaults(func=user)

message_parser = subparsers.add_parser("message", help="Get message")
message_parser.add_argument("-l", "--line_num", help="Number of line to parse")
message_parser.set_defaults(func=message)

random_logs_parser = subparsers.add_parser("random-logs", help="Get n random logs")
random_logs_parser.add_argument("-n", "--number", help="Number of logs to get")
random_logs_parser.set_defaults(func=random_logs)

frequency_parser = subparsers.add_parser("frequency", help="Get frequency of logs")
frequency_parser.set_defaults(func=frequency)

global_stats_parser = subparsers.add_parser("global-stats", help="Get global stats")
global_stats_parser.set_defaults(func=global_statistics)

user_stats_parser = subparsers.add_parser("user-stats", help="Get user stats")
user_stats_parser.add_argument("-u", "--user", help="User to get stats for")
user_stats_parser.set_defaults(func=user_statistics)


args = parser.parse_args()
args.func()
