from ormar import BigInteger, Integer, Model, String
from sqlalchemy import PrimaryKeyConstraint

from .metadata import BaseMeta

__all__ = ("CommandLog",)


class CommandLog(Model):
    class Meta(BaseMeta):
        tablename = "commands"
        constraints = [PrimaryKeyConstraint("command", "guild", "channel", "member")]

    # pyright: reportGeneralTypeIssues=false
    command: str = String(max_length=255, primary_key=True)
    guild: int = BigInteger()
    channel: int = BigInteger()
    member: int = BigInteger()
    amount: int = BigInteger(default=1)


# ormar :(
CommandLog.command.primary_key = True
CommandLog.guild.primary_key = True
CommandLog.channel.primary_key = True
CommandLog.member.primary_key = True
