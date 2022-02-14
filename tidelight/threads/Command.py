import enum
from dataclasses import dataclass


class CommandType(enum.Enum):
    STOP = enum.auto


@dataclass
class Command:
    command_type: CommandType
    payload: ...
