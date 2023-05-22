from __future__ import annotations

from ..botbase import BotBase
from ..db import CommandLog
from ..models import CogBase
from ..wraps import MyInter


class CommandLogging(CogBase[BotBase]):
    @CogBase.listener()
    async def on_application_command_completion(self, inter: MyInter):
        assert inter.application_command is not None

        assert inter.channel is not None

        cmd = inter.application_command.name
        guild = inter.guild.id if inter.guild is not None else None
        channel = inter.channel.id if inter.guild is not None else None
        member = inter.user.id

        # Incrementing amount without funky sub queries is not possible.
        await CommandLog.raw(
            """
            INSERT INTO command_log (command, guild, channel, member, amount)
            VALUES ({}, {}, {}, {}, 1)
            ON CONFLICT (command, guild, channel, member)
            DO UPDATE SET amount = command_log.amount + 1;
            """,
            cmd,
            guild,
            channel,
            member,
        )


def setup(bot: BotBase):
    bot.add_cog(CommandLogging(bot))
