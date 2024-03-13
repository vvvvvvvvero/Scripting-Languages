import re

LOG_TIMESTAMP = 'Timestamp'
LOG_HOST = 'Host'
LOG_ID = 'Id'
LOG_MESSAGE = 'Message'
LOG_PATTERN = r'(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[(\d+)\]:\s([^\n]+)'

ACCEPTED_MESSAGE = 'udane logowanie'
SESSION_OPENED_MESSAGE = 'sesja otwarta'
FAILED_MESSAGE = 'nieudane logowanie'
DISCONNECT_MESSAGE = 'zamknięcie połączenia'
SESSION_CLOSED_MESSAGE = 'sesja zamknięta'
INVALID_USER_MESSAGE = 'bledna nazwa uzytkownika'
BREAK_IN_ATTEMPT_MESSAGE = 'próba włamania'


def parse_ssh_log(log_string: str) -> dict:
    log_match = re.match(LOG_PATTERN, log_string)
    if log_match:
        return {
            LOG_TIMESTAMP: log_match.group(1),
            LOG_HOST: log_match.group(2),
            LOG_ID: log_match.group(3),
            LOG_MESSAGE: log_match.group(4)
        }
    else:
        return {}


if __name__ == '__main__':
    print(parse_ssh_log('Dec 10 11:42:04 LabSZ sshd[28143]:'
                        ' Received disconnect from 183.62.140.253: 11: Bye Bye [preauth]'))
