from log_entries import SSHFailedPasswordEntry, SSHErrorEntry, SSHAcceptedPasswordEntry, SSHOtherEntry
from log_journal import SSHLogJournal
from ipaddress import IPv4Address
import pytest


def test_time_extraction():
    error_log = SSHErrorEntry('Jan  7 11:04:31 LabSZ sshd[28334]: error: Received disconnect from 103.207.36.21:'
                              ' 3: com.jcraft.jsch.JSchException: Auth fail [preauth]')
    assert error_log.timestamp == 'Jan  7 11:04:31'


def test_valid_ipv4_address():
    failed_log = SSHFailedPasswordEntry('Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for'
                                        ' invalid user webmaster from 173.234.31.186 port 38926 ssh2')
    assert failed_log.get_ip4_address() == IPv4Address('173.234.31.186')


def test_invalid_ipv4_address():
    failed_log = SSHFailedPasswordEntry('Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for'
                                        ' invalid user webmaster from 666.777.88.213 port 38926 ssh2')
    assert failed_log.get_ip4_address() is None


def test_no_ipv4_address():
    failed_log = SSHFailedPasswordEntry('Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for'
                                        ' invalid user webmaster from port 38926 ssh2')
    assert failed_log.get_ip4_address() is None


@pytest.mark.parametrize('log_string, expected_type', [
    ('Jan  6 16:19:00 LabSZ sshd[30097]: Failed password for invalid user admin from 185.222.209.151 port 42314 ssh2',
     SSHFailedPasswordEntry),
    ('Jan  7 13:02:21 LabSZ sshd[29169]: Accepted password for curi from 123.255.103.215 port 60751 ssh2',
     SSHAcceptedPasswordEntry),
    ('Jan  7 11:04:31 LabSZ sshd[28334]: error: Received disconnect from'
     ' 103.207.36.21: 3: com.jcraft.jsch.JSchException: Auth fail [preauth]', SSHErrorEntry),
    ('Dec 10 07:08:30 LabSZ sshd[24208]: Connection closed by 103.207.36.21 [preauth]', SSHOtherEntry),
])
def test_append(log_string, expected_type):
    journal = SSHLogJournal()
    log = journal.append(log_string)
    assert isinstance(log, expected_type)
