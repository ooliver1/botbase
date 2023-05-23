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

        # await CommandLog.insert(
        #     CommandLog(
        #         {
        #             CommandLog.command: cmd,
        #             CommandLog.guild: guild,
        #             CommandLog.channel: channel,
        #             CommandLog.member: member,
        #         }
        #     )
        # ).on_conflict(
        #     (
        #         CommandLog.command,
        #         CommandLog.guild,
        #         CommandLog.channel,
        #         CommandLog.member,
        #     ),
        #     "DO UPDATE",
        #     ((CommandLog.amount, Unquoted("command_log.amount + 1")),),
        # )
        await CommandLog.raw(
            """INSERT INTO command_log
            VALUES ({}, {}, {}, {}, 1)
            ON CONFLICT (command, guild, channel, member)
            DO UPDATE
            SET amount = command_log.amount + 1
        """
        )


def setup(bot: BotBase):
    bot.add_cog(CommandLogging(bot))
