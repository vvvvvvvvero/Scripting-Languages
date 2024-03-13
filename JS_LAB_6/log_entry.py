from utils import *
from abc import ABC, abstractmethod
from datetime import datetime
from ipaddress import IPv4Address
from typing import Dict, Optional


class SSHLogEntry(ABC):
    def __init__(self, log_string: str) -> None:
        self.log_dict: Dict[str, str] = parse_ssh_log(log_string)
        self.timestamp: str = self.log_dict[LOG_TIMESTAMP]
        self.host: str = self.log_dict[LOG_HOST]
        self.__message: str = self.log_dict[LOG_MESSAGE]
        self.pid_number: str = self.log_dict[LOG_PID_NUMBER]

    def __str__(self) -> str:
        return f'[{self.timestamp}] [{self.host}] [{self.pid_number}] [{self.message}]'

    @abstractmethod
    def validate(self) -> bool:
        pass

    @property
    def message(self) -> str:
        return self.__message

    def get_ip4_address(self) -> Optional[IPv4Address]:
        ip4_address = get_ip4_address(self.log_dict)
        if is_valid_ip4_address(ip4_address):
            return IPv4Address(ip4_address)
        else:
            return None

    def get_user(self) -> Optional[str]:
        return get_user(self.log_dict)

    @property
    def has_ip(self) -> bool:
        return self.get_ip4_address() is not None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(timestamp={self.timestamp}, host={self.host}, ' \
               f'pid_number={self.pid_number}, message={self.message}),'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SSHLogEntry):
            raise TypeError(f'Cannot compare {self.__class__.__name__} with {other.__class__.__name__}')
        return self.log_dict.items() == other.log_dict.items()

    def __lt__(self, other: 'SSHLogEntry') -> bool:
        if not isinstance(other, SSHLogEntry):
            raise TypeError(f'Cannot compare {self.__class__.__name__} with {other.__class__.__name__}')
        return datetime.strptime(self.timestamp, DATE_FORMAT) < datetime.strptime(other.timestamp, DATE_FORMAT)

    def __gt__(self, other: 'SSHLogEntry') -> bool:
        if not isinstance(other, SSHLogEntry):
            raise TypeError(f'Cannot compare {self.__class__.__name__} with {other.__class__.__name__}')
        return datetime.strptime(self.timestamp, DATE_FORMAT) > datetime.strptime(other.timestamp, DATE_FORMAT)
