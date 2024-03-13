import sys
from datetime import datetime
from nasa_log_utils import convert_bytes


def read_log():
    entries = []
    for line in sys.stdin:
        fields = line.strip().split()
        host = fields[0]
        date = datetime.strptime(fields[3][1:], '%d/%b/%Y:%H:%M:%S')
        http_code = int(fields[-2])
        size = convert_bytes(fields[-1])

        if len(fields) < 10:
            path = fields[-3]
        else:
            path = fields[-4]

        entry = (host, date, path, http_code, size)
        entries.append(entry)

    return entries


if __name__ == "__main__":
    log_info = read_log()
    print(log_info)
