from log_entry import SSHLogEntry
from log_entries import SSHAcceptedPasswordEntry, SSHFailedPasswordEntry, SSHErrorEntry, SSHOtherEntry
import os
from typing import List, Iterator, Type


class SSHLogJournal:
    def __init__(self) -> None:
        self.ssh_log_list: List[SSHLogEntry] = []

    def __len__(self) -> int:
        return len(self.ssh_log_list)

    def __iter__(self) -> Iterator[SSHLogEntry]:
        return iter(self.ssh_log_list)

    def __contains__(self, log: SSHLogEntry) -> bool:
        return log in self.ssh_log_list

    def append(self, log_string: str) -> SSHLogEntry:
        log: SSHLogEntry = self.__create_log(log_string)
        if log.validate():
            self.ssh_log_list.append(log)
            return log
        else:
            raise ValueError("Log entry is not valid")

    def load_log_file(self) -> None:
        file_path: str = input("Enter path to log file: ")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    self.append(line)
        else:
            print("File does not exist")

    def __create_log(self, log_string: str) -> SSHLogEntry:
        log_type: Type[SSHLogEntry] = self.__determine_log_type(log_string)
        return log_type(log_string)

# może być statyczny ponieważ nie używa żadnych zmiennych instancji ani nie modyfikuje stanu obiektu

    @staticmethod
    def __determine_log_type(log_string: str) -> Type[SSHLogEntry]:
        if "Failed password" in log_string:
            return SSHFailedPasswordEntry
        elif "Accepted password" in log_string:
            return SSHAcceptedPasswordEntry
        elif "error:" in log_string:
            return SSHErrorEntry
        else:
            return SSHOtherEntry

    def filter_by_ip(self, ip_address: str) -> List[SSHLogEntry]:
        return [log for log in self.ssh_log_list if str(log.get_ip4_address()) == ip_address]

    def filter_by_user(self, username: str) -> List[SSHLogEntry]:
        return [log for log in self.ssh_log_list if username == log.get_user()]

    def get_log_by_index(self, index: int) -> SSHLogEntry:
        if index < 0 or index >= len(self.ssh_log_list):
            raise IndexError("Index out of range")
        return self.ssh_log_list[index]


if __name__ == '__main__':
    log_journal = SSHLogJournal()

    log1 = log_journal.append('Jan  7 11:04:31 LabSZ sshd[28334]: error: Received disconnect from'
                              ' 103.207.36.21: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]')
    log2 = log_journal.append('Jan  7 13:02:21 LabSZ sshd[29169]: Accepted password for'
                              ' curi from 123.255.103.215 port 60751 ssh2')
    log3 = log_journal.append('Jan  6 16:19:00 LabSZ sshd[30097]: Failed password for'
                              ' invalid user admin from 185.222.209.151 port 42314 ssh2')
    log4 = log_journal.append('Dec 10 07:08:30 LabSZ sshd[24208]: Connection closed by 103.207.36.21 [preauth]')

    for entry in log_journal:
        print(entry)

    other_log = SSHOtherEntry('Dec 10 07:07:38 LabSZ sshd[24206]: input_userauth_request: invalid user test9 [preauth]')

    print(log_journal.__len__())
    print(log_journal.__contains__(log4))
    print(log_journal.__contains__(other_log))

    print(len(log_journal))
    print(log1 in log_journal)

    filtered_ip = log_journal.filter_by_ip('103.207.36.21')
    filtered_user = log_journal.filter_by_user('curi')

    for ip in filtered_ip:
        print(ip)
    for user in filtered_user:
        print(user)

    for i in range(len(log_journal)):
        print(f'{i + 1}. ', log_journal.get_log_by_index(i), f'-> {log_journal.get_log_by_index(i).__class__.__name__}')
