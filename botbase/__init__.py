from logging import NullHandler, getLogger
from typing import NamedTuple, Literal


__version__ = "0.0.0a"


getLogger(__name__).addHandler(NullHandler())


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=0, minor=0, micro=0, releaselevel="alpha", serial=0)
