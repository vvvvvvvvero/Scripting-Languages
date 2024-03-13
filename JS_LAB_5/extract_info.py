from utils import *
from process_ssh_log import *

IPV4_REGEX = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
USER_REGEX = re.compile(r'user\s+(?P<user>\w+)')
SUCCESS_USER_REGEX = re.compile(r'(?:Accepted|Failed) password for (?P<user>\w+)')

MESSAGE_TYPE_DICT = {
    r'Accepted password for': ACCEPTED_MESSAGE,
    r'session opened for': SESSION_OPENED_MESSAGE,
    r'Failed password for': FAILED_MESSAGE,
    r'Received disconnect': DISCONNECT_MESSAGE,
    r'Connection closed by': DISCONNECT_MESSAGE,
    r'session closed for': SESSION_CLOSED_MESSAGE,
    r'Invalid user': INVALID_USER_MESSAGE,
    r"POSSIBLE BREAK-IN ATTEMPT!": BREAK_IN_ATTEMPT_MESSAGE,
}


def get_ipv4s_from_log(ssh_log) -> list:
    ipv4_list = IPV4_REGEX.findall(ssh_log[LOG_MESSAGE])
    return ipv4_list


def get_user_from_log(ssh_log) -> str:
    user = USER_REGEX.search(ssh_log[LOG_MESSAGE])
    if not user:
        user = SUCCESS_USER_REGEX.search(ssh_log[LOG_MESSAGE])
    return user.group('user') if user else None


def get_message_type_from_log(ssh_log) -> str:
    for regex, message_type in MESSAGE_TYPE_DICT.items():
        if re.search(regex, ssh_log[LOG_MESSAGE]):
            return message_type
    return 'inne'


if __name__ == '__main__':
    for log in get_log_dict_list():
        print(get_message_type_from_log(log))
