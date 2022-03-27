from __future__ import annotations

from difflib import get_close_matches
from itertools import groupby
from sys import stderr
from traceback import print_exception
from typing import TYPE_CHECKING, cast
from logging import getLogger

from nextcord import ButtonStyle, Embed, Interaction
from nextcord.ext.commands import Cog, HelpCommand
from nextcord.ext.menus import ButtonMenuPages, ListPageSource, PageSource
from nextcord.ui import Select, Button
from nextcord.utils import format_dt
from botbase import MyContext, BotBase, MyInter

if TYPE_CHECKING:
    from nextcord.ext.commands import Command, Group
    from nextcord.ui import Item


log = getLogger(__name__)


class MyMenu(ButtonMenuPages):
    ctx: MyContext
    interaction: MyInter


class MultiSource(ListPageSource):
    def __init__(
        self, multi: Group | Cog, commands: list[Command], *, prefix: str | None = None
    ):
        super().__init__(entries=commands, per_page=5)
        self.multi = multi
        self.prefix = prefix
        self.title = f"{self.multi.qualified_name.capitalize()} Commands"
        self.description = self.multi.description

    def format_page(self, menu: MyMenu, commands: list[Command]) -> Embed:
        ctx = menu.ctx if menu.ctx else menu.interaction
        embed = Embed(
            title=self.title,
            description=f"{self.description}\n{ctx.bot.helpinsert}",
            color=ctx.bot.color,
        )
        for command in commands:
            name = command.qualified_name
            signature = f"{self.prefix}{name} {command.signature}"
            embed.add_field(
                name=signature,
                value=command.short_doc or "N/A",
                inline=False,
            )

        maximum = self.get_max_pages()
        if maximum > 1:
            embed.set_author(
                name=f"Page {menu.current_page + 1}/{maximum} "
                f"({len(self.entries)} commands)"
            )

        embed.set_footer(text=f"Use `{self.prefix}help <command>` for more info.")

        return embed


class FrontPageSource(PageSource):
    def is_paginating(self) -> bool:
        return True

    def get_max_pages(self) -> int:
        return 2

    async def get_page(self, num: int) -> FrontPageSource:
        self.index = num
        return self

    def format_page(self, menu: MyMenu, _) -> Embed:
        bt = (
            menu.ctx.bot
            if menu.ctx
            else menu.interaction.client
            if menu.interaction
            else False
        )
        if not bt:
            raise RuntimeError("Why are we here just to suffer?")

        clean_prefix = menu.ctx.clean_prefix if menu.ctx else "/"

        bot = cast(BotBase, bt)
        assert bot.user is not None

        embed = Embed(
            title=bot.helptitle.format(name=bot.user.name),
            description=bot.helpmsg.format(prefix=clean_prefix, name=bot.user.name),
            color=bot.color,
        )

        for name, value in bot.helpfields.items():
            embed.add_field(
                name=name,
                value=value,
                inline=False,
            )

        created_at = format_dt(bot.user.created_at, "F")
        if self.index == 0:
            embed.add_field(
                name="Who are you?",
                value=bot.helpindex.format(created_at=created_at),
                inline=False,
            )
        elif self.index == 1:
            entries: tuple[tuple[str, str], ...] = (
                ("<arg>", "This means the arg is __**required**__."),
                ("[arg]", "This means the arg is __**optional**__."),
                ("{A|B}", "This means that it can be __**either A or B**__."),
                (
                    "[arg...]",
                    "This means you can have multiple args.\n"
                    "__**You do not type in the brackets!**__",
                ),
            )

            embed.add_field(
                name="How Do I Use You?", value="Here is how the help command works:"
            )

            for name, value in entries:
                embed.add_field(name=name, value=value, inline=False)

        return embed


class HelpSelect(Select["HelpView"]):
    def __init__(
        self, commands: dict[Cog | Group, list[Command]], bot: BotBase
    ) -> None:
        super().__init__(
            placeholder="Select a category...", min_values=1, max_values=1, row=0
        )
        self.commands = commands
        self.bot = bot
        self.fill()

    def fill(self) -> None:
        self.add_option(
            label="Index",
            emoji=self.bot.emojiset.index,
            value="index",
            description="The main page on how to use the bot!",
        )
        for cog, commands in self.commands.items():
            if not commands or cog.qualified_name in ("Jishaku", "help"):
                continue
            description = cog.description or None
            emoji = getattr(cog, "emoji", None)
            self.add_option(
                label=cog.qualified_name.capitalize(),
                emoji=emoji,
                value=cog.qualified_name,
                description=description,
            )

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        value = self.values[0]
        if value == "index":
            await self.view.change_source(FrontPageSource())
            await interaction.response.pong()
        else:
            cog = self.bot.get_cog(value)
            if cog is None:
                await interaction.response.send_message(
                    "Somehow that doesn't exist...", ephemeral=True
                )
                return

            commands = self.commands[cog]
            if not commands:
                await interaction.response.send_message(
                    "That category is empty!", ephemeral=True
                )
                return

            source = MultiSource(cog, commands, prefix=self.view._ctx.clean_prefix)
            await self.view.change_source(source)
            await interaction.response.pong()


class HelpView(ButtonMenuPages):
    def __init__(
        self, source: PageSource, ctx: MyContext, cmds: dict[Cog | Group, list[Command]]
    ) -> None:
        super().__init__(source=source, style=ButtonStyle.blurple)
        if len(cmds) != 1:
            # HACK
            children = self.children.copy()
            for child in children:
                self.remove_item(child)
            self.add_item(HelpSelect(cmds, ctx.bot))
            for child in children:
                self.add_item(child)
            # HACK

        self.ctx = ctx
        self._ctx = ctx

    async def on_error(
        self, error: Exception, item: Item, interaction: Interaction
    ) -> None:
        if interaction.response.is_done():
            await interaction.followup.send(
                "An unknown error occurred, sorry", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "An unknown error occurred, sorry", ephemeral=True
            )
        print_exception(type(error), error, error.__traceback__, file=stderr)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user and interaction.user.id in (
            self._ctx.bot.owner_id,
            self._ctx.author.id,
        ):
            return True
        await interaction.response.send_message(
            f"This menu is for {self._ctx.author.mention}, use {self._ctx.clean_prefix}help to have a menu to yourself.",
            ephemeral=True,
        )
        return False

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, Button) or isinstance(child, Select):
                child.disabled = True

        if self.message is not None:
            await self.message.edit(view=self)

    async def _set_all_disabled(self, disable: bool):
        for child in self.children:
            if isinstance(child, Button) or isinstance(child, Select):
                child.disabled = disable
        await self._update_view()


class MyHelp(HelpCommand):
    context: MyContext

    def get_command_signature(self, command: Command | Group) -> str:
        name = command.qualified_name
        return f"{self.context.clean_prefix}{name} {command.signature}"

    async def send_bot_help(self, mapping: dict[Cog, Command]) -> None:
        bot = self.context.bot

        if coggie := bot.get_cog("Help"):
            mapping.pop(coggie)

        def key(command) -> str:
            cog = command.cog
            return cog.qualified_name if cog else "\U0010ffff"

        entries: list[Command] = [
            c for c in sorted(bot.commands, key=key) if not c.hidden
        ]

        all_commands: dict[Cog, list[Command]] = {}
        for name, children in groupby(entries, key=key):
            if name == "U0010ffff":
                continue

            cog = bot.get_cog(name)
            if cog is not None:
                all_commands[cog] = sorted(children, key=lambda c: c.qualified_name)

        menu = HelpView(FrontPageSource(), ctx=self.context, cmds=all_commands)  # type: ignore
        if isinstance(self.context, Interaction):
            await menu.start(interaction=self.context)
        else:
            await menu.start(self.context)

    async def send_cog_help(self, cog: Cog):
        entries: list[Command] = [
            c
            for c in sorted(cog.get_commands(), key=lambda c: c.qualified_name)
            if not c.hidden
        ]
        menu = HelpView(
            source=MultiSource(cog, prefix=self.context.clean_prefix, commands=entries),
            cmds={cog: entries},
            ctx=self.context,
        )
        if isinstance(self.context, Interaction):
            await menu.start(interaction=self.context)
        else:
            await menu.start(self.context)

    async def send_command_help(self, command):
        embed = Embed(colour=self.context.bot.color)
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group: Group):
        subcommands = list(group.commands)
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = [c for c in subcommands if not c.hidden]
        if len(entries) == 0:
            return await self.send_command_help(group)

        source = MultiSource(group, entries, prefix=self.context.clean_prefix)
        self.common_command_formatting(source, group)
        menu = HelpView(source, ctx=self.context, cmds={group: entries})
        if isinstance(self.context, Interaction):
            await menu.start(interaction=self.context)
        else:
            await menu.start(self.context)

    async def send_error_message(self, error: Exception) -> None:
        if "command" in self.context.kwargs:
            cmd = self.context.kwargs["command"]
            cmds = [cmd.name for cmd in self.context.bot.commands if not cmd.hidden]
            matches = get_close_matches(cmd, cmds)
            if len(matches) > 0:
                msg = f'Command "`{cmd}`" not found, maybe you meant "`{matches[0]}`"?'
            else:
                msg = f'Command "`{cmd}`" not found, try {self.context.clean_prefix}help to see available commands.'
        else:
            msg = str(error)
        embed = Embed(title="Error", description=msg, color=self.context.bot.color)
        await self.context.send_embed("Error", msg)

    def common_command_formatting(
        self, embed: Embed | MultiSource, command: Command
    ) -> None:
        embed.title = self.get_command_signature(command)
        if command.description:
            embed.description = f"{command.description}\n\n{command.help}"
        else:
            embed.description = command.help or "No help found..."

        if isinstance(embed, Embed):
            if command.aliases:
                embed.add_field(
                    name="Aliases", value=", ".join(command.aliases), inline=False
                )
            if e := command.extras.get("example"):
                embed.add_field(name="Example", value=e, inline=False)


class Help(Cog, name="help", description="Get some help!"):
    def __init__(self, bot: BotBase):
        self.bot = bot
        bot.help_command = MyHelp()
        bot.help_command.cog = self

    # @property
    # def emoji(self) -> str:
    #     return self.bot.emojiset.help


def setup(bot: BotBase):
    bot.add_cog(Help(bot))
