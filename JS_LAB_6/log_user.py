import re
from utils import DATE_FORMAT
from datetime import datetime
from log_journal import SSHLogJournal
USER_PATTERN = r'^[a-zA-Z0-9_-]{3,20}$'


class SSHUser:
    def __init__(self, username, last_login):
        self.username = username
        self.last_login = datetime.strptime(last_login, DATE_FORMAT)

    def __str__(self):
        return f'{self.username} {self.last_login}'

    def validate(self):
        return re.match(USER_PATTERN, self.username) is not None

    def update_last_login(self, last_login):
        self.last_login = datetime.strptime(last_login, DATE_FORMAT)


if __name__ == "__main__":
    log_journal = SSHLogJournal()
    log_journal.append('Dec 10 19:22:22 LabSZ sshd[19465]:'
                       ' Accepted password for curi from 137.189.241.19 port 4300 ssh2')
    log_journal.append('Dec 10 07:07:38 LabSZ sshd[24206]: pam_unix(sshd:auth): check pass; user unknown')
    log_journal.append('Dec 12 22:50:08 LabSZ sshd[31757]:'
                       ' Accepted password for fztu from 119.137.63.195 port 50945 ssh2')

    user1 = SSHUser("user25", "Jan  9 22:13:44")
    user2 = SSHUser("u", "Jan 10 01:12:33")
    user3 = SSHUser("user!", "Jan 11 22:13:44")

    shared_list = [log_journal.get_log_by_index(0), user1, log_journal.get_log_by_index(1),
                   user2, user3, log_journal.get_log_by_index(2)]
    for item in shared_list:
        print(item.validate())
