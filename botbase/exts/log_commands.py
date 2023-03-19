from __future__ import annotations

from typing import TYPE_CHECKING

from ormar import NoMatch

from ..botbase import BotBase
from ..db import CommandLog, database
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

        # Composite PK not in ormar ruins the whole SQL statement.
        await database.execute(
            """
            INSERT INTO commands (command, guild, channel, member, amount)
            VALUES (:command, :guild, :channel, :member, 1)
            ON CONFLICT (command, guild, channel, member)
            DO UPDATE SET amount = commands.amount + 1
            """,
            {
                "command": cmd,
                "guild": guild,
                "channel": channel,
                "member": member,
            },
        )


def setup(bot: BotBase):
    bot.add_cog(CommandLogging(bot))
