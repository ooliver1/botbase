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


__version__ = "1.14.2"


getLogger(__name__).addHandler(NullHandler())
