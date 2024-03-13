import re
LOG_PATTERN = r'(\w{3}\s+\d+\s\d+:\d+:\d+)\s(\w+)\ssshd\[(\d+)\]:\s([^\n]+)'
IPV4_REGEX = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
USER_REGEX = re.compile(r'user\s+(?P<user>\w+)')
SUCCESS_USER_REGEX = re.compile(r'(?:Accepted|Failed) password for (?P<user>\w+)')

LOG_TIMESTAMP = 'Timestamp'
LOG_HOST = 'Host'
LOG_ID = 'Id'
LOG_MESSAGE = 'Message'
USER = 'User'
IP = 'IP'


class LogUtils:
    def __init__(self):
        self.logs = []
        self.filtered_logs = []

    def load_log_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                self.logs.append(line.strip())
        return self.logs

    @staticmethod
    def parse_log(log_line):
        log_match = re.match(LOG_PATTERN, log_line)
        if log_match:
            return {
                LOG_TIMESTAMP: log_match.group(1),
                LOG_HOST: log_match.group(2),
                LOG_ID: log_match.group(3),
                LOG_MESSAGE: log_match.group(4),
                IP: LogUtils.get_ip_from_log(log_line),
                USER: LogUtils.get_user_from_log(log_line)
            }
        else:
            return {}

    def filter_logs(self, logs_to_filter, start_time, end_time):
        for log_entry in logs_to_filter:
            log_dict = self.parse_log(log_entry)
            if start_time <= log_dict[LOG_TIMESTAMP] <= end_time:
                self.filtered_logs.append(log_entry)
        return self.filtered_logs

    @staticmethod
    def get_user_from_log(log_line) -> str:
        user = USER_REGEX.search(log_line)
        if not user:
            user = SUCCESS_USER_REGEX.search(log_line)
        return user.group('user') if user else None

    @staticmethod
    def get_ip_from_log(log_line) -> str:
        ips = IPV4_REGEX.findall(log_line)
        return ", ".join(ips)


if __name__ == "__main__":
    log = LogUtils()
    logs = log.load_log_file("/Users/veraemelianova/PycharmProjects/JS_LAB_8/SSH.log")
    print(LogUtils.parse_log(logs[1]))

