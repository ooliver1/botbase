from logging import NullHandler, getLogger

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
from .models import CogBase

__version__ = "1.16.2"


getLogger(__name__).addHandler(NullHandler())
