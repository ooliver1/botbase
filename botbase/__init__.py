from logging import NullHandler, getLogger
from typing import NamedTuple, Literal


from .botbase import BotBase
from .emojis import Emojis
from .exceptions import Blacklisted
from .wraps import (
    MyContext,
    MyInter,
    WrappedChannel,
    WrappedMember,
    WrappedUser,
    WrappedThread,
    Wrap,
)
from .checks import *


__version__ = "1.8.0"


getLogger(__name__).addHandler(NullHandler())


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="alpha", serial=0)
