from log_entry import SSHLogEntry
from utils import get_user, get_port, get_error_message, LOG_MESSAGE


class SSHFailedPasswordEntry(SSHLogEntry):
    def __init__(self, log_string: str) -> None:
        super().__init__(log_string)
        self.username: str = get_user(self.log_dict)
        self.port: str = get_port(self.log_dict)

    def validate(self) -> bool:
        return "Failed password" in self.message and self.username in self.message and self.port in self.message


class SSHAcceptedPasswordEntry(SSHLogEntry):
    def __init__(self, log_string: str) -> None:
        super().__init__(log_string)
        self.username: str = get_user(self.log_dict)
        self.port: str = get_port(self.log_dict)

    def validate(self) -> bool:
        return "Accepted password" in self.message and self.username in self.message and self.port in self.message


class SSHErrorEntry(SSHLogEntry):
    def __init__(self, log_string: str) -> None:
        super().__init__(log_string)
        self.error_message: str = get_error_message(self.log_dict)

    def validate(self) -> bool:
        return self.error_message in self.message


class SSHOtherEntry(SSHLogEntry):
    def __init__(self, log_string: str) -> None:
        super().__init__(log_string)
        self.other_message: str = self.log_dict[LOG_MESSAGE]

    def validate(self) -> bool:
        return True


if __name__ == '__main__':
    log1 = SSHErrorEntry('Jan  7 11:04:31 LabSZ sshd[28334]: error: Received disconnect from 103.207.36.21:'
                         ' 3: com.jcraft.jsch.JSchException: Auth fail [preauth]')
    log2 = SSHAcceptedPasswordEntry('Jan  7 13:02:21 LabSZ sshd[29169]:'
                                    ' Accepted password for curi from 123.255.103.215 port 60751 ssh2')
    log3 = SSHFailedPasswordEntry('Jan  6 16:19:00 LabSZ sshd[30097]:'
                                  ' Failed password for invalid user admin from 185.222.209.151 port 42314 ssh2')
    log4 = SSHOtherEntry('Dec 10 07:08:30 LabSZ sshd[24208]: Connection closed by 500.234.31.186 [preauth]')

    print(log1.message)
    print(log1.error_message)
    print(log1.validate())

    print(log2.message)
    print(log2.username)
    print(log2.port)
    print(log2.validate())

    print(log3.has_ip)
    print(log4.has_ip)

    print(log1.__repr__())
    print(log2 == log3)
    print(log2 == log2)
    print(log1 < log2)
    print(log3 > log2)



