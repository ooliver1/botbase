"""
CREATE TABLE IF NOT EXISTS commands (
    command VARCHAR NOT NULL,
    guild BIGINT,
    channel BIGINT,
    member BIGINT NOT NULL,
    amount INT,
    UNIQUE(command, guild, channel, member)
);

if not self.db_enabled:
    return

if inter.guild is not None:
    await self.db.execute(
        INSERT INTO commands (command, guild, channel, member, amount) 
        VALUES ($1,$2,$3,$4,$5) 
        ON CONFLICT (command, guild, channel, member) DO UPDATE
            SET amount = commands.amount + 1,
        inter.command,
        inter.guild.id,
        inter.channel.id,  # type: ignore
        inter.author.id,
        1,
    )
else:
    a = await self.db.fetchval(
        "SELECT * FROM commands WHERE member=$1 AND channel IS NULL and guild IS NULL",
        inter.author.id,
    )
    if a is None:
        await self.db.execute(
            INSERT INTO commands (command, guild, channel, member, amount) 
            VALUES ($1,$2,$3,$4,$5),
            inter.command,
            None,
            None,
            inter.author.id,
            1,
        )
    else:
        await self.db.execute(
            UPDATE commands SET amount = commands.amount + 1 
            WHERE member=$1 AND channel IS NULL and guild IS NULL,
            inter.author.id,
        )
"""
from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from nextcord import Embed, Guild, Object, slash_command
from nextcord.ext.application_checks import is_owner
from ormar import BigInteger, Model, String

from ..botbase import BotBase
from ..db import BaseMeta
from ..models import CogBase
from ..wraps import MyInter

if TYPE_CHECKING:
    from ..botbase import BotBase


_log = getLogger(__name__)


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
