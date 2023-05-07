from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

from nextcord import Embed

from ..botbase import BotBase
from ..models import CogBase

if TYPE_CHECKING:
    from nextcord import Guild


class GuildLogging(CogBase[BotBase]):
    @CogBase.listener()
    async def on_guild_join(self, guild: Guild):
        if not self.bot.log_channel:
            return

        assert guild.owner_id is not None

        embed = Embed(
            title="New Guild!",
            description=dedent(
                f"""

        **{guild.name}**
        id: `{guild.id}`
        members: `{guild.member_count}`
        owner: `{guild.owner or await self.bot.fetch_user(guild.owner_id)}`

        """
            ),
            color=self.bot.colour,
        )
        try:
            await self.bot.get_channel(self.bot.log_channel).send(embed=embed)  # type: ignore
        except AttributeError:
            pass

    @CogBase.listener()
    async def on_guild_remove(self, guild: Guild):
        if guild.unavailable:
            return

        if not self.bot.log_channel:
            return

        assert guild.owner_id is not None

        embed = Embed(
            title="Removed Guild :(",
            description=dedent(
                f"""

        **{guild.name}**
        id: `{guild.id}`
        members: `{guild.member_count}`
        owner: `{guild.owner or await self.bot.fetch_user(guild.owner_id)}`

        """
            ),
            color=self.bot.colour,
        )
        try:
            await self.bot.get_channel(self.bot.log_channel).send(embed=embed)  # type: ignore
        except AttributeError:
            pass


def setup(bot: BotBase) -> None:
    bot.add_cog(GuildLogging(bot))
