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


__version__ = "1.11.6"


getLogger(__name__).addHandler(NullHandler())


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=1, minor=8, micro=3, releaselevel="final", serial=0)
