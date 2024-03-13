import math
from extract_info import *
import random
import statistics
from collections import Counter
from datetime import datetime

DATE_FORMAT = "%b %d %H:%M:%S"


def get_all_users(log_dict: list) -> list:
    user_list = []
    for entry in log_dict:
        user = get_user_from_log(entry)
        if user not in user_list and user is not None and user != 'unknown':
            user_list.append(user)
    return user_list


def get_logs_for_user(log_dict: list, user: str) -> list:
    user_logs = []
    for entry in log_dict:
        if get_user_from_log(entry) == user:
            user_logs.append(entry)
    return user_logs


def get_n_random_user_logs(log_dict: list, n: int) -> list:
    user_list = get_all_users(log_dict)
    random_user = random.choice(user_list)
    print('Random user: ' + random_user)
    user_logs = get_logs_for_user(log_dict, random_user)
    random_logs = random.sample(user_logs, n if n < len(user_logs) else len(user_logs))
    return random_logs


def get_logging_attempts(log_dict: list) -> list:
    logging_attempts = []
    for entry in log_dict:
        user = get_user_from_log(entry)
        if get_message_type_from_log(entry) == ACCEPTED_MESSAGE or get_message_type_from_log(entry) == FAILED_MESSAGE:
            logging_attempts.append(user)
    return logging_attempts


def get_most_and_least_frequent_user(log_dict: list) -> tuple:
    user_list = get_logging_attempts(log_dict)
    user_counter = Counter(user_list)
    most_frequent_user = user_counter.most_common(1)[0][0]
    least_frequent_user = user_counter.most_common()[-1][0]
    print(f'Most frequent user: {most_frequent_user} with {user_counter[most_frequent_user]} attempts')
    print(f'Least frequent user: {least_frequent_user} with {user_counter[least_frequent_user]} attempts')
    return most_frequent_user, least_frequent_user


def find_connection_closed_for_log(log_entry, logs_to_process: list) -> dict:
    target_user = get_user_from_log(log_entry)
    for entry in logs_to_process:
        if target_user == get_user_from_log(entry) and get_message_type_from_log(entry) == SESSION_CLOSED_MESSAGE:
            return entry


def calculate_connection_time(log_entry, log_dict: list):
    logs_to_process = log_dict[log_dict.index(log_entry) + 1:]
    connection_closed_log = find_connection_closed_for_log(log_entry, logs_to_process)
    if connection_closed_log is None:
        return None
    start_time = datetime.strptime(log_entry[LOG_TIMESTAMP], DATE_FORMAT)
    end_time = datetime.strptime(connection_closed_log[LOG_TIMESTAMP], DATE_FORMAT)
    return math.ceil(((end_time - start_time).seconds / 60) * 100) / 100


def get_connection_time_list(log_dict: list) -> list:
    connection_time_list = []
    for entry in log_dict:
        if get_message_type_from_log(entry) == SESSION_OPENED_MESSAGE and get_user_from_log(entry) is not None:
            connection_time = calculate_connection_time(entry, log_dict)
            if connection_time is not None:
                connection_time_list.append(connection_time)
    return connection_time_list


def get_average_time_global(log_dict: list):
    connection_durations = get_connection_time_list(log_dict)
    print(f'Mean: {get_mean_and_st_dev(connection_durations)[0]} minutes and standard deviation:'
          f' {get_mean_and_st_dev(connection_durations)[1]} minutes for all users')
    return get_mean_and_st_dev(connection_durations)


def get_average_time_for_user(log_dict: list, user: str):
    user_logs = get_logs_for_user(log_dict, user)
    connection_durations = get_connection_time_list(user_logs)
    if len(connection_durations) == 0:
        print(f'No ssh session found for user {user}')
        return None
    print(f'Mean: {get_mean_and_st_dev(connection_durations)[0]} minutes and standard deviation:'
          f' {get_mean_and_st_dev(connection_durations)[1]} minutes for user {user}')
    return get_mean_and_st_dev(connection_durations)


def get_mean_and_st_dev(connection_time_list: list):
    if len(connection_time_list) > 1:
        connection_mean = statistics.mean(connection_time_list)
        connection_st_dev = statistics.stdev(connection_time_list)
        return math.ceil(connection_mean * 100) / 100, math.ceil(connection_st_dev * 100) / 100
    elif len(connection_time_list) == 1:
        return connection_time_list[0], 0
    else:
        return None


if __name__ == '__main__':
    logs = get_log_dict_list()
    r_logs = get_most_and_least_frequent_user(logs)
    print(r_logs)
