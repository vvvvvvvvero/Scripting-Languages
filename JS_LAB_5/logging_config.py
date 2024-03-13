import logging
import sys
from extract_info import *


log_format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s")
error_format = logging.Formatter("%(asctime)s - [%(levelname)s] - %(message)s - %(filename)s")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(log_format)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(error_format)
stderr_handler.setLevel(logging.ERROR)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


def log_num_of_bytes(log_line: str):
    logger.debug(f'Liczba przeczytanych bajtów: {len(log_line)}')


def process_log(log_line: str):
    log_line_dict = parse_ssh_log(log_line)
    log_num_of_bytes(log_line)
    message_type = get_message_type_from_log(log_line_dict)
    if message_type == ACCEPTED_MESSAGE:
        logger.info("Udane logowanie")
    elif message_type == SESSION_OPENED_MESSAGE:
        logger.info("Sesja otwarta")
    elif message_type == FAILED_MESSAGE:
        logger.warning("Nieudane logowanie")
    elif message_type == SESSION_CLOSED_MESSAGE:
        logger.info("Sesja zamknieta")
    elif message_type == DISCONNECT_MESSAGE:
        logger.info("Zamknięcie połączenia")
    elif message_type == INVALID_USER_MESSAGE:
        logger.error("Błędna nazwa użytkownika")
    elif message_type == BREAK_IN_ATTEMPT_MESSAGE:
        logger.critical("Próba włamania")


def process_logs():
    for line in get_log_list():
        process_log(line)


if __name__ == '__main__':
    process_logs()
