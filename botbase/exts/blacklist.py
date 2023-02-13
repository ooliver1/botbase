from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from nextcord import Embed, Guild, slash_command
from nextcord.ext.application_checks import is_owner

from ..botbase import BotBase
from ..db import BlacklistGuild, BlacklistUser
from ..models import CogBase
from ..wraps import MyInter

if TYPE_CHECKING:
    from ..botbase import BotBase


_log = getLogger(__name__)


class Blacklist:
    def __init__(self) -> None:
        self.guilds = set()
        self.users: set = set()

    def __contains__(self, obj: int) -> bool:
        assert isinstance(obj, int)

        return obj in self.guilds or obj in self.users

    async def add(
        self, obj: int, reason: str = "Unknown reason", guild: bool = False
    ) -> None:
        assert isinstance(obj, int)

        if guild:
            self.guilds.add(obj)
            await BlacklistGuild.objects.create(id=obj, reason=reason)
        else:
            self.users.add(obj)
            await BlacklistUser.objects.create(id=obj, reason=reason)

    async def remove(self, obj: int, guild: bool = False) -> None:
        assert isinstance(obj, int)

        if guild:
            self.guilds.discard(obj)
            await BlacklistGuild.objects.delete(id=obj)
        else:
            self.users.discard(obj)
            await BlacklistUser.objects.delete(id=obj)

    async def load(self) -> None:
        self.guilds = set(await BlacklistGuild.objects.values_list("id", flatten=True))
        self.users = set(await BlacklistUser.objects.values_list("id", flatten=True))


class BlacklistCog(CogBase[BotBase]):
    def __init__(self, bot: BotBase) -> None:
        super().__init__(bot)

        self.blacklist = Blacklist()
        bot.loop.create_task(self.load_blacklist())
        self.old_process_application_commands = bot.process_application_commands
        bot.process_application_commands = self.check  # type: ignore  # MyInter + Interaction

        if bot.guild_ids:
            self.blacklist_.guild_ids_to_rollout.update(bot.guild_ids)

    async def load_blacklist(self) -> None:
        await self.bot.wait_until_ready()

        await self.blacklist.load()

    async def check(self, interaction: MyInter) -> None:
        if interaction.guild_id in self.blacklist.guilds:
            return _log.info("Ignoring blacklisted Guild(id=%s)", interaction.guild_id)

        if interaction.user.id in self.blacklist.users:
            return _log.info("Ignoring blacklisted User(id=%s)", interaction.user.id)

        await self.old_process_application_commands(interaction)

    def cog_unload(self) -> None:
        self.bot.process_application_commands = self.old_process_application_commands

    @CogBase.listener()
    async def on_guild_join(self, guild: Guild):
        if guild.id in self.blacklist.guilds:
            _log.info("Leaving blacklisted Guild(id=%s)", guild.id)
            await guild.leave()
            return

    @slash_command(name="blacklist", description="Blacklist a user or guild.")
    @is_owner()
    async def blacklist_(self, inter: MyInter) -> None:
        ...

    @blacklist_.subcommand(name="add")
    async def blacklist_add(self, inter: MyInter) -> None:
        ...

    @blacklist_add.subcommand(name="user", description="Blacklist a user.")
    async def blacklist_add_user(self, inter: MyInter, user: str) -> None:
        await self.blacklist.add(int(user), guild=False)
        await inter.response.send_message(
            embed=Embed(
                description=f"I have added <@{user}> to the blacklist.",
                color=self.bot.colour,
            ),
            ephemeral=True,
        )

    @blacklist_add.subcommand(name="guild", description="Blacklist a guild.")
    async def blacklist_add_guild(self, inter: MyInter, guild: str) -> None:
        await self.blacklist.add(int(guild), guild=True)
        await inter.response.send_message(
            embed=Embed(
                description=f"I have added `{guild}` to the blacklist.",
                color=self.bot.colour,
            ),
            ephemeral=True,
        )

    @blacklist_.subcommand(name="remove")
    async def blacklist_remove(self, inter: MyInter) -> None:
        ...

    @blacklist_remove.subcommand(
        name="user", description="Remove a user from the blacklist."
    )
    async def blacklist_remove_user(self, inter: MyInter, user: str) -> None:
        await self.blacklist.remove(int(user), guild=False)
        await inter.response.send_message(
            embed=Embed(
                description=f"I have removed <@{user}> from the blacklist.",
                color=self.bot.colour,
            ),
            ephemeral=True,
        )

    @blacklist_remove.subcommand(
        name="guild", description="Remove a guild from the blacklist."
    )
    async def blacklist_remove_guild(self, inter: MyInter, guild: str) -> None:
        await self.blacklist.remove(int(guild), guild=True)
        await inter.response.send_message(
            embed=Embed(
                description=f"I have removed `{guild}` from the blacklist.",
                color=self.bot.colour,
            ),
            ephemeral=True,
        )

    @blacklist_.subcommand(
        name="list", description="List all blacklisted users and guilds."
    )
    async def blacklist_list(self, inter: MyInter) -> None:
        if self.blacklist.users:
            user_blacklists = "\n".join(f"`{u}`" for u in self.blacklist.users)
        else:
            user_blacklists = "No user's blacklisted."

        if self.blacklist.guilds:
            guild_blacklists = "\n".join(f"`{g}`" for g in self.blacklist.guilds)
        else:
            guild_blacklists = "No guild's blacklisted."

        await inter.response.send_message(
            embed=Embed(
                title="Blacklists",
                description=f"Users:\n{user_blacklists}\n\nGuilds:\n{guild_blacklists}",
            ),
            ephemeral=True,
        )


def setup(bot: BotBase):
    bot.add_cog(BlacklistCog(bot))
