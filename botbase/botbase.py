from __future__ import annotations

from asyncio import TimeoutError as AsyncTimeoutError
from asyncio import wait_for
from contextlib import suppress
from logging import CRITICAL, INFO, Formatter, StreamHandler, getLogger
from logging.handlers import RotatingFileHandler
from pathlib import Path
from random import choice
from sys import modules
from types import ModuleType
from typing import TYPE_CHECKING

from aiohttp import BaseConnector, BasicAuth, ClientSession
from nextcord import Intents, Interaction, Member, Thread, User, abc
from nextcord.ext.commands import AutoShardedBot, ExtensionNotFound
from nextcord.utils import MISSING

from .wraps import MyInter, WrappedChannel, WrappedMember, WrappedThread, WrappedUser

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from typing import Any, Awaitable, Callable, Iterable, Mapping, Sequence, Union

    from nextcord import (
        AllowedMentions,
        BaseActivity,
        Guild,
        MemberCacheFlags,
        Message,
        PartialMessageable,
        Status,
    )
    from nextcord.ext.commands import Bot, HelpCommand

    _NonCallablePrefix = Union[str, Sequence[str]]


log = getLogger(__name__)


def get_handlers():
    formatter = Formatter(
        "%(levelname)-7s %(asctime)s %(filename)12s:%(funcName)-28s: %(message)s",
        datefmt="%H:%M:%S %d/%m/%Y",
    )
    h = RotatingFileHandler(
        "./logs/bot/io.log",
        maxBytes=1000000,
        backupCount=5,
        encoding="utf-8",
    )
    i = StreamHandler()

    i.setFormatter(formatter)
    h.setFormatter(formatter)
    h.namer = lambda name: name.replace(".log", "") + ".log"
    return h, i


class BotBase(AutoShardedBot):
    session: ClientSession

    @staticmethod
    def get_module() -> str:
        file = modules["__main__"].__file__

        if file is None:
            raise RuntimeError("how")

        path = Path(file)

        if path.parts[-1] == "__main__.py":
            return path.parts[-2]

        return "."

    def __init__(
        self,
        command_prefix: Union[
            _NonCallablePrefix,
            Callable[
                [Union[Bot, AutoShardedBot], Message],
                Union[Awaitable[_NonCallablePrefix], _NonCallablePrefix],
            ],
        ] = tuple(),
        *,
        version: str = "0.0.0",
        aiohttp_enabled: bool = True,
        blacklist_enabled: bool = True,
        db_enabled: bool = True,
        colours: list[int] = [0x9966CC],
        name: str | None = None,
        log_channel: int | None = None,
        guild_ids: Sequence[int] | None = None,
        log_commands: bool = True,
        log_guilds: bool = False,
        # nextcord
        help_command: HelpCommand | None = None,
        description: str | None = None,
        max_messages: int | None = 1000,
        connector: BaseConnector | None = None,
        proxy: str | None = None,
        proxy_auth: BasicAuth | None = None,
        shard_id: int | None = None,
        shard_count: int | None = None,
        shard_ids: list[int] | None = None,
        application_id: int | None = None,
        intents: Intents = Intents.default(),
        member_cache_flags: MemberCacheFlags = MISSING,
        chunk_guilds_at_startup: bool = MISSING,
        status: Status | None = None,
        activity: BaseActivity | None = None,
        allowed_mentions: AllowedMentions | None = None,
        heartbeat_timeout: float = 60.0,
        guild_ready_timeout: float = 2.0,
        assume_unsync_clock: bool = True,
        enable_debug_events: bool = False,
        loop: AbstractEventLoop | None = None,
        lazy_load_commands: bool = True,
        rollout_associate_known: bool = True,
        rollout_delete_unknown: bool = True,
        rollout_register_new: bool = True,
        rollout_update_known: bool = True,
        rollout_all_guilds: bool = False,
        default_guild_ids: list[int] | None = None,
        owner_id: int | None = None,
        owner_ids: Iterable[int] | None = None,
        strip_after_prefix: bool = False,
        case_insensitive: bool = False,
        **kwargs: Any,  # fallback for missing args
    ) -> None:
        super().__init__(
            command_prefix=command_prefix,
            help_command=help_command,
            description=description,
            max_messages=max_messages,
            connector=connector,
            proxy=proxy,
            proxy_auth=proxy_auth,
            shard_id=shard_id,
            shard_count=shard_count,
            shard_ids=shard_ids,
            application_id=application_id,
            intents=intents,
            member_cache_flags=member_cache_flags,
            chunk_guilds_at_startup=chunk_guilds_at_startup,
            status=status,
            activity=activity,
            allowed_mentions=allowed_mentions,
            heartbeat_timeout=heartbeat_timeout,
            guild_ready_timeout=guild_ready_timeout,
            assume_unsync_clock=assume_unsync_clock,
            enable_debug_events=enable_debug_events,
            loop=loop,
            lazy_load_commands=lazy_load_commands,
            rollout_associate_known=rollout_associate_known,
            rollout_delete_unknown=rollout_delete_unknown,
            rollout_register_new=rollout_register_new,
            rollout_update_known=rollout_update_known,
            rollout_all_guilds=rollout_all_guilds,
            default_guild_ids=default_guild_ids,
            owner_id=owner_id,
            owner_ids=owner_ids,
            strip_after_prefix=strip_after_prefix,
            case_insensitive=case_insensitive,
            **kwargs,
        )
        self.module = self.get_module()

        self.prefix: dict[int, list[str]] = {}

        log = getLogger()
        log.handlers = []
        log.setLevel(INFO)
        h, i = get_handlers()

        log.addHandler(h)
        log.addHandler(i)
        getLogger("asyncio").setLevel(CRITICAL)

        self.loop.set_exception_handler(self.asyncio_handler)

        self.version: str = version
        self.aiohttp_enabled: bool = aiohttp_enabled
        self.colours: list[int] = colours
        self.name: str | None = name
        self.db_enabled: bool = db_enabled
        self.log_channel: int | None = log_channel
        self.guild_ids: Sequence[int] | None = guild_ids

        self._single_events: dict[str, Callable] = {
            "on_message": self.get_wrapped_message,
            "on_interaction": self.get_wrapped_interaction,
        }
        self._double_events: dict[str, Callable] = {
            "on_message_edit": lambda before, after: (
                self.get_wrapped_message(before),
                self.get_wrapped_message(after),
            )
        }

        self.load_extension("delarva", extras={"guild_ids": guild_ids})

        if blacklist_enabled and db_enabled:
            self.load_extension("botbase.exts.blacklist")

        if log_commands and db_enabled:
            self.load_extension("botbase.exts.log_commands")

        if log_guilds:
            self.load_extension("botbase.exts.log_guilds")

    @property
    def colour(self) -> int:
        return choice(self.colours)

    def asyncio_handler(self, _, context: dict) -> None:
        log = getLogger("notasyncio")
        if context["message"] == "Unclosed client session":
            return

        log.error(
            context["message"]
            + "\n"
            + "\n".join(
                f"{k}: {v}"
                for k, v in context.items()
                if k != "message" and k is not None and v is not None and k != "None"
            )
        )

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        if self.db_enabled:
            from .db import database

            await database.connect()

        if self.aiohttp_enabled:
            self.session = ClientSession()

        await super().start(token, reconnect=reconnect)

    def run(self, token: str, *, reconnect: bool = True) -> None:
        cogs = Path(self.module)

        for ext in cogs.glob("exts/**/*.py"):
            log.info("Found file %s", ext)
            if any(part.startswith("_") for part in ext.parts):
                continue

            if ext.suffix == ".py":
                a = ".".join(ext.parts).removesuffix(".py")
                log.info("Loading ext %s", a)
                self.load_extension(a)
                log.info("Loaded ext %s", a)

        super().run(token, reconnect=reconnect)

    async def close(self, *args, **kwargs) -> None:
        if self.aiohttp_enabled and hasattr(self, "session"):
            await self.session.close()

        if self.db_enabled:
            with suppress(AsyncTimeoutError):
                from .db import database

                await wait_for(database.disconnect(), timeout=5)

        await super().close(*args, **kwargs)

    async def on_application_command_error(*_):
        ...  # hope an event handler exists

    async def on_interaction(self, interaction: Interaction) -> None:
        i = self.get_wrapped_interaction(interaction)

        await self.process_application_commands(i)

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
        channel: Union[
            abc.GuildChannel, abc.PrivateChannel, Thread, PartialMessageable
        ],
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

    def get_wrapped_interaction(self, inter: Interaction) -> MyInter:
        i = MyInter(inter, self)
        if i.user:
            i.user = self.get_wrapped_person(i.user)

        i.author = i.user

        return i

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

    def load_extension(
        self, name: str, *, extras: dict[str, Any] | None = None
    ) -> None:
        ext = f"{self.name}.exts.{name}" if self.name else name

        try:
            super().load_extension(ext, extras=extras)
        except (ExtensionNotFound, ModuleNotFoundError):
            super().load_extension(name, extras=extras)

        if self.is_ready():
            self.loop.create_task(self.sync_all_application_commands())

    def reload_extension(self, name: str) -> None:
        ext = f"{self.name}.exts.{name}" if self.name else name

        try:
            super().reload_extension(ext)
        except (ExtensionNotFound, ModuleNotFoundError):
            super().reload_extension(name)

        if self.is_ready():
            self.loop.create_task(self.sync_all_application_commands())

    def unload_extension(self, name: str) -> None:
        ext = f"{self.name}.exts.{name}" if self.name else name

        try:
            super().unload_extension(ext)
        except (ExtensionNotFound, ModuleNotFoundError):
            super().unload_extension(name)

        self.loop.create_task(self.sync_all_application_commands())

    @property
    def extensions(self) -> Mapping[str, ModuleType]:
        if not self.name:
            return super().extensions

        return {
            k.removeprefix(f"{self.name}.exts."): v
            for k, v in super().extensions.items()
        } | super().extensions
