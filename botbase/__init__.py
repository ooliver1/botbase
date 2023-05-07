from logging import NullHandler, getLogger
from os import getenv

if getenv("DB_URI"):
    from .db import *

from .botbase import *
from .models import *
from .wraps import *

__version__ = "2.0.2"  # x-release-please-version


getLogger(__name__).addHandler(NullHandler())
