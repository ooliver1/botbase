from logging import NullHandler, getLogger

from .botbase import *
from .db import *
from .exts import *
from .models import *
from .wraps import *

__version__ = "1.22.3"  # x-release-please-version


getLogger(__name__).addHandler(NullHandler())
