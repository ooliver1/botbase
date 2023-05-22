from logging import getLogger

from piccolo.table import Table
from piccolo.columns import BigInt, Text, Integer

log = getLogger(__name__)
__all__ = ("CommandLog",)


class CommandLog(Table):
    command = Text(primary_key=True)
    guild = BigInt()
    channel = BigInt()
    member = BigInt()
    amount = Integer(default=1)
