from ormar import BigInteger, Integer, Model, String
from sqlalchemy import UniqueConstraint

from .metadata import BaseMeta

__all__ = ("CommandLog",)


class CommandLog(Model):
    class Meta(BaseMeta):
        tablename = "commands"
        constraints = [UniqueConstraint("command", "guild", "channel", "member")]

    # pyright: reportGeneralTypeIssues=false
    id: int = String(primary_key=True, autoincrement=False)
    command: str = String(max_length=255)
    guild: int = BigInteger()
    channel: int = BigInteger()
    member: int = BigInteger()
    amount: int = BigInteger(default=1)
