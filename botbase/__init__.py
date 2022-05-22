from logging import NullHandler, getLogger
from typing import Literal, NamedTuple

from .botbase import BotBase, get_handler
from .checks import *
from .emojis import Emojis
from .exceptions import Blacklisted
from .wraps import (
    MyContext,
    MyInter,
    Wrap,
    WrappedChannel,
    WrappedMember,
    WrappedThread,
    WrappedUser,
)

__version__ = "1.14.7"


getLogger(__name__).addHandler(NullHandler())
