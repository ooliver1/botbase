from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from ormar import BigInteger, Model, String

from ..botbase import BotBase
from ..db import BaseMeta
from ..models import CogBase
from ..wraps import MyInter

if TYPE_CHECKING:
    from ..botbase import BotBase


class CommandLog(Model):
    class Meta(BaseMeta):
        tablename = "commands"

    # pyright: reportGeneralTypeIssues=false
    command: str = String(max_length=255, primary_key=True)
    guild: int = BigInteger(primary_key=True, autoincrement=False)
    channel: int = BigInteger(primary_key=True, autoincrement=False)
    member: int = BigInteger(primary_key=True, autoincrement=False)
    amount: int = BigInteger(default=1)


class CommandLogging(CogBase[BotBase]):
    @CogBase.listener()
    async def on_application_command_completion(self, inter: MyInter):
        assert inter.application_command is not None

        assert inter.channel is not None
        entry, created = await CommandLog.objects.get_or_create(
            command=inter.application_command.name,
            guild=inter.guild.id if inter.guild is not None else None,
            channel=inter.channel.id if inter.guild is not None else None,
            member=inter.author.id,
        )
        if not created:
            entry.amount += 1
            await entry.save()


def setup(bot: BotBase):
    bot.add_cog(CommandLogging(bot))
