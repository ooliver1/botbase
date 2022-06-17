from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import Embed, Object
from nextcord.ext.commands import group, is_owner

from ..models import CogBase
from ..wraps import MyContext

if TYPE_CHECKING:
    from ..botbase import BotBase


class BlacklistCog(CogBase):
    @group(invoke_without_command=True, hidden=True)
    @is_owner()
    async def blacklist(self, ctx: MyContext) -> None:
        await ctx.send_help(ctx.command)

    @blacklist.group(invoke_without_command=True)
    @is_owner()
    async def add(self, ctx: MyContext) -> None:
        await ctx.send_help(ctx.command)

    @add.command(name="person", aliases=["user"])
    @is_owner()
    async def add_person(self, ctx: MyContext, user: Object, *, reason=None) -> None:
        assert self.bot.blacklist is not None
        await self.bot.blacklist.add(user.id, reason=reason, guild=False)
        await ctx.send_embed(description=f"I have added <@{user.id}> to the blacklist.")

    @add.command(name="guild", aliases=["server"])
    @is_owner()
    async def add_guild(self, ctx: MyContext, guild: Object, *, reason=None) -> None:
        assert self.bot.blacklist is not None
        await self.bot.blacklist.add(guild.id, reason=reason, guild=True)
        await ctx.send_embed(description=f"I have added the guild `{guild.id}` to the blacklist")

    @blacklist.command()
    @is_owner()
    async def list(self, ctx: MyContext) -> None:
        assert self.bot.blacklist is not None
        if self.bot.blacklist.users:
            user_blacklists = "\n".join(f"`{u}`" for u in self.bot.blacklist.users)
        else:
            user_blacklists = "No user's blacklisted."

        if self.bot.blacklist.guilds:
            guild_blacklists = "\n".join(f"`{g}`" for g in self.bot.blacklist.guilds)
        else:
            guild_blacklists = "No guild's blacklisted."

        await ctx.send(
            embed=Embed(
                title="Blacklists",
                description=f"Users:\n{user_blacklists}\n\nGuilds:\n{guild_blacklists}",
            )
        )

    @blacklist.group(invoke_without_command=True)
    @is_owner()
    async def remove(self, ctx: MyContext) -> None:
        await ctx.send_help(ctx.command)

    @remove.command(name="person", aliases=["user"])
    @is_owner()
    async def remove_person(self, ctx: MyContext, user: Object) -> None:
        assert self.bot.blacklist is not None
        await self.bot.blacklist.remove(user.id, guild=False)
        await ctx.send_embed("I have completed that action for you.")

    @remove.command(name="guild", aliases=["server"])
    @is_owner()
    async def remove_guild(self, ctx: MyContext, guild: Object) -> None:
        assert self.bot.blacklist is not None
        await self.bot.blacklist.remove(guild.id, guild=True)
        await ctx.send_embed("I have completed that action for you.")


def setup(bot: BotBase):
    bot.add_cog(BlacklistCog(bot))
