from __future__ import annotations

from importlib import import_module
from logging import CRITICAL, INFO, Formatter, getLogger
from logging.handlers import RotatingFileHandler
from textwrap import dedent
from typing import TYPE_CHECKING

import jishaku
from aiohttp import ClientSession
from asyncpg import create_pool
from nextcord import Embed, Member, Thread, User, abc
from nextcord.ext.commands import Bot, when_mentioned_or

from .blacklist import Blacklist
from .emojis import Emojis
from .exceptions import Blacklisted
from .wraps import MyContext, WrappedChannel, WrappedMember, WrappedThread, WrappedUser

if TYPE_CHECKING:
    from typing import Any, Callable, Union

    from asyncpg import Pool
    from nextcord import Guild, Message


log = getLogger(__name__)
defaulthelpmsg = """
HI! Welcome to the help page for {name}!

Use `{prefix}help <command>` for more info on a command,
or `{prefix}help <category>` for more info on a category,

Use the dropdown below to select a category.

Have fun!
"""
defaulthelpindex = """
I have been up since {created_at} and I serve for you!
"""


class BotBase(Bot):
    db: Pool
    session: ClientSession
    blacklist: Blacklist

    def __init__(self, *args, config_module: str = "config", **kwargs) -> None:
        pre = kwargs.pop("command_prefix", self.get_pre)

        super().__init__(*args, command_prefix=pre, **kwargs)

        self.prefix: dict[int, list[str]] = {}

        log = getLogger()
        log.handlers = []
        log.setLevel(INFO)
        h = RotatingFileHandler(
            "./logs/bot/io.log",
            maxBytes=1000000,
            backupCount=5,
            encoding="utf-8",
        )
        h.setFormatter(
            Formatter(
                "%(levelname)-7s %(asctime)s %(filename)12s:%(funcName)-16s: %(message)s",
                datefmt="%H:%M:%S %d/%m/%Y",
            )
        )
        h.namer = lambda name: name.replace(".log", "") + ".log"
        log.addHandler(h)
        getLogger("asyncio").setLevel(CRITICAL)

        self.loop.set_exception_handler(self.asyncio_handler)

        config = import_module(config_module.rstrip(".py"))

        self.db_enabled: bool
        self.db_args: tuple[Any, ...]
        self.db_kwargs: dict[str, Any]

        if db_url := getattr(config, "db_url", None):
            self.db_enabled = True
            self.db_args = (db_url,)
            self.db_kwargs = {}
        elif (db_name := getattr(config, "db_name", None)) and (
            db_user := getattr(config, "db_user", "ooliver")
        ):
            self.db_enabled = True
            self.db_args = ()
            self.db_kwargs = {
                "database_name": db_name,
                "user": db_user,
            }
        else:
            self.db_enabled = False
            self.db_args = ()
            self.db_kwargs = {}

        self.version: str = getattr(config, "version", "0.0.0")
        self.aiohttp_enabled: bool = getattr(config, "aiohttp_enabled", True)
        self.color: int = getattr(config, "color", 0x9966CC)
        self.blacklist_enabled: bool = getattr(config, "blacklist_enabled", True)
        self.default_pre: list[str] = getattr(config, "prefix")
        self.helpmsg: str = getattr(config, "helpmsg", defaulthelpmsg)
        self.helpindex: str = getattr(config, "helpindex", defaulthelpindex)
        self.helpfields: dict[str, str] = getattr(config, "helpfields", {})
        self.helptitle: str = getattr(config, "helptitle", "Help Me!")
        self.emojiset: Any = getattr(config, "emojiset", Emojis())
        self.logchannel: int = getattr(config, "logchannel", 921139782648725515)

        self._single_events: dict[str, Callable] = {
            "on_message": self.get_wrapped_message,
        }
        self._double_events: dict[str, Callable] = {
            "on_message_edit": lambda before, after: (
                self.get_wrapped_message(before),
                self.get_wrapped_message(after),
            )
        }

        self.load_extension("jishaku")
        self.load_extension("botbase.coggies.help")

        if self.blacklist_enabled:
            self.load_extension("botbase.coggies.blacklist")

        self.loop.create_task(self.startup())

    def asyncio_handler(self, loop, context):
        log = getLogger("notasyncio")
        if context["message"] == "Unclosed client session":
            return

        log.error(
            context["message"]
            + "\n"
            + "\n".join(
                f"{k}: {v}"
                for k, v in context.items()
                if k != "message" and k is not None and v is not None
            )
        )

    async def startup(self) -> None:
        if self.db_enabled:
            db = await create_pool(*self.db_args, **self.db_kwargs)
            assert db is not None
            self.db = db

        if self.aiohttp_enabled:
            self.session = ClientSession()

        if self.blacklist_enabled:
            self.blacklist = Blacklist(self.db)

    def run(self, *args, **kwargs) -> None:
        self.loop.create_task(self.startup())

        super().run(*args, **kwargs)

    async def close(self, *args, **kwargs) -> None:
        if self.aiohttp_enabled:
            await self.session.close()

        await super().close(*args, **kwargs)

    @staticmethod
    async def get_pre(bot: BotBase, message: Message) -> list[str]:
        if message.guild is not None:
            try:
                prefix = bot.prefix[message.guild.id]
            except KeyError:
                prefix = [
                    await bot.db.fetchval(
                        "SELECT prefix FROM guilds WHERE id=$1", message.guild.id
                    )
                ]
                if prefix[0] is None:
                    prefix = bot.default_pre
                bot.prefix[message.guild.id] = prefix
        else:
            prefix = bot.default_pre
        return when_mentioned_or(*prefix)(bot, message)

    async def process_commands(self, message: Message) -> None:
        if message.author.bot:
            return

        if message.author.id in self.blacklist:
            raise Blacklisted("Ignoring blacklisted user")
        elif message.guild and message.guild.id in self.blacklist:
            raise Blacklisted("Ignoring blacklisted guild")

        ctx = await self.get_context(message, cls=MyContext)

        await self.invoke(ctx)

    async def getch_member(self, guild_id: int, member_id: int) -> WrappedMember:
        guild = await self.getch_guild(guild_id)
        member = guild.get_member(member_id)
        if member is not None:
            return WrappedMember(member, bot=self)

        member = await guild.fetch_member(member_id)
        return WrappedMember(member, bot=self)

    async def getch_channel(self, channel_id: int) -> WrappedChannel | WrappedThread:
        channel = self.get_channel(channel_id)
        if channel:
            return self.get_wrapped_channel(channel)

        channel = await self.fetch_channel(channel_id)
        return self.get_wrapped_channel(channel)

    async def getch_guild(self, guild_id: int) -> Guild:
        guild = self.get_guild(guild_id)
        if guild:
            return guild

        guild = await self.fetch_guild(guild_id)
        return guild

    async def getch_user(self, user_id: int) -> WrappedUser:
        user = self.get_user(user_id)
        if user:
            return WrappedUser(user, bot=self)

        user = await self.fetch_user(user_id)
        return WrappedUser(user, self)

    def get_wrapped_channel(
        self,
        channel: Union[abc.GuildChannel, abc.PrivateChannel, Thread],
    ) -> Union[WrappedThread, WrappedChannel]:
        if isinstance(channel, Thread):
            return WrappedThread(channel, self)

        return WrappedChannel(channel, self)

    def get_wrapped_person(
        self, person: Union[User, Member]
    ) -> Union[WrappedUser, WrappedMember]:
        if isinstance(person, Member):
            return WrappedMember(person, self)

        return WrappedUser(person, self)

    def get_wrapped_message(self, message: Message) -> Message:
        message.channel = self.get_wrapped_channel(message.channel)  # type: ignore
        message.author = self.get_wrapped_person(message.author)

        return message

    def dispatch(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        _name = f"on_{event_name}"
        if _name in self._single_events:
            wrapped_arg = self._single_events[_name](args[0])
            super().dispatch(event_name, wrapped_arg)

        elif _name in self._double_events:
            wrapped_first_arg, wrapped_second_arg = self._double_events[_name](
                args[0], args[1]
            )
            super().dispatch(event_name, wrapped_first_arg, wrapped_second_arg)

        else:
            super().dispatch(event_name, *args, **kwargs)

    async def on_command_completion(self, ctx: MyContext):
        if ctx.guild is None:
            guild_id = None
            channel_id = None
        else:
            guild_id = ctx.guild.id
            channel_id = ctx.channel.id

        if ctx.guild is not None:
            await self.db.execute(
                """INSERT INTO commands (command, guild, channel, member, amount) 
                VALUES ($1,$2,$3,$4,$5) 
                ON CONFLICT (command, guild, channel, member) DO UPDATE
                    SET amount = commands.amount + 1""",
                ctx.command.qualified_name,  # type: ignore
                guild_id,
                channel_id,
                ctx.author.id,
                1,
            )
        else:
            a = await self.db.fetchval(
                "SELECT * FROM commands WHERE member=$1", ctx.author.id
            )
            if a is None:
                await self.db.execute(
                    """INSERT INTO commands (command, guild, channel, member, amount) 
                    VALUES ($1,$2,$3,$4,$5)""",
                    ctx.command.qualified_name,  # type: ignore
                    guild_id,
                    channel_id,
                    ctx.author.id,
                    1,
                )
            else:
                await self.db.execute(
                    """UPDATE commands SET amount = commands.amount + 1 
                    WHERE member=$1""",
                    ctx.author.id,
                )

    async def on_guild_join(self, guild: Guild):
        if guild.id in self.blacklist.guilds:
            log.info("Leaving blacklisted Guild(id=%s)", guild.id)
            await guild.leave()
            return

        embed = Embed(
            title="New Guild!",
            description=dedent(
                f"""

        **{guild.name}**
        id: `{guild.id}`
        members: `{guild.member_count}`

        """
            ),
            color=self.color,
        )
        await self.get_channel(self.logchannel).send(embed=embed)  # type: ignore

    async def on_guild_remove(self, guild: Guild):
        if guild.unavailable:
            return

        embed = Embed(
            title="Removed Guild :(",
            description=dedent(
                f"""

        **{guild.name}**
        id: `{guild.id}`
        members: `{guild.member_count}`

        """
            ),
            color=self.color,
        )
        try:
            await self.get_channel(self.logchannel).send(embed=embed)  # type: ignore
        except AttributeError:
            pass
