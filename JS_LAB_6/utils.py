import re
from ipaddress import IPv4Address
from typing import Dict, Optional, Match

LOG_TIMESTAMP = 'Timestamp'
LOG_HOST = 'Host'
LOG_PID_NUMBER = 'Id'
LOG_MESSAGE = 'Message'
LOG_PATTERN = r'(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[(\d+)\]:\s([^\n]+)'
IPV4_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
USER_REGEX = re.compile(r'user\s+(?P<user>\w+)')
SUCCESS_USER_REGEX = re.compile(r'(?:Accepted|Failed) password for (?P<user>\w+)')
PORT_PATTERN = r'port\s+(?P<port>\d+)'
ERROR_PATTERN = r'error:\s+(?P<error>.+?) \['
DATE_FORMAT = "%b %d %H:%M:%S"

matchType = Optional[Match[str]]


def parse_ssh_log(log_string: str) -> Dict[str, str]:
    log_match: matchType = re.match(LOG_PATTERN, log_string)
    if log_match:
        return {
            LOG_TIMESTAMP: log_match.group(1),
            LOG_HOST: log_match.group(2),
            LOG_PID_NUMBER: log_match.group(3),
            LOG_MESSAGE: log_match.group(4)
        }
    else:
        return {}


def get_ip4_address(log_entry: Dict[str, str]) -> str:
    ip4_match: matchType = re.search(IPV4_PATTERN, log_entry[LOG_MESSAGE])
    if ip4_match:
        return ip4_match.group(1)
    else:
        return ""


def get_user(log_entry: Dict[str, str]) -> str:
    user: matchType = USER_REGEX.search(log_entry[LOG_MESSAGE])
    if not user:
        user = SUCCESS_USER_REGEX.search(log_entry[LOG_MESSAGE])
    return user.group('user') if user else ""


def get_port(log_entry: Dict[str, str]) -> str:
    port_match: matchType = re.search(PORT_PATTERN, log_entry[LOG_MESSAGE])
    if port_match:
        return port_match.group('port')
    else:
        return ""


def get_error_message(log_entry: Dict[str, str]) -> str:
    error_match: matchType = re.search(ERROR_PATTERN, log_entry[LOG_MESSAGE])
    if error_match:
        return error_match.group('error')
    else:
        return ""


def is_valid_ip4_address(ip4_address: Optional[str]) -> bool:
    try:
        IPv4Address(ip4_address)
        return True
    except ValueError:
        return False
