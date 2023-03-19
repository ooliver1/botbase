from __future__ import annotations

from typing import TYPE_CHECKING

from ormar import NoMatch

from ..botbase import BotBase
from ..db import CommandLog
from ..models import CogBase
from ..wraps import MyInter

if TYPE_CHECKING:
    from ..botbase import BotBase


class CommandLogging(CogBase[BotBase]):
    @CogBase.listener()
    async def on_application_command_completion(self, inter: MyInter):
        assert inter.application_command is not None

        assert inter.channel is not None

        cmd = inter.application_command.name
        guild = inter.guild.id if inter.guild is not None else None
        channel = inter.channel.id if inter.guild is not None else None
        member = inter.user.id

        try:
            entry = await CommandLog.objects.get(
                command=cmd,
                guild=guild,
                channel=channel,
                member=member,
            )
        except NoMatch:
            await CommandLog.objects.create(
                command=cmd,
                guild=guild,
                channel=channel,
                member=member,
            )
        else:
            entry.amount += 1
            await entry.update()


def setup(bot: BotBase):
    bot.add_cog(CommandLogging(bot))
