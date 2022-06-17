from __future__ import annotations

from typing import Any, Callable, Coroutine, TypeVar, Union, cast

from nextcord import BaseApplicationCommand, ClientUser, Interaction, User
from nextcord.ext.application_checks import check as app_check
from nextcord.ext.commands import (
    BotMissingPermissions,
    Command,
    Context,
    GuildChannelConverter,
    MissingPermissions,
    NoPrivateMessage,
    bot_has_guild_permissions,
    bot_has_permissions,
    check,
    has_guild_permissions,
    has_permissions,
)

from .wraps.context import MyContext
from .wraps.inter import MyInter

__all__ = (
    "admin_owner_perms",
    "admin_owner_perms_a",
    "bot_admin_perms",
    "bot_admin_perms_a",
    "admin_owner_guild_perms",
    "admin_owner_guild_perms_a",
    "bot_admin_guild_perms",
    "bot_admin_guild_perms_a",
    "admin_owner_or_channel_perms",
    "admin_owner_or_channel_perms_a",
    "bot_admin_or_channel_perms",
    "bot_admin_or_channel_perms_a",
    "admin_owner_or_arg_perms",
    "admin_owner_or_arg_perms_a",
    "bot_admin_or_arg_perms",
    "bot_admin_or_arg_perms_a",
)


T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]
MaybeCoro = Union[T, Coro[T]]
CT = TypeVar("CT", bound=Union[Interaction, Context])
CH = TypeVar("CH", BaseApplicationCommand, Command, CoroFunc)


def admin_owner_perms_p(func: Callable[[Callable], Any]):
    def decorator(**perms: bool):
        """user has admin or is me or permissions"""

        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.author, User):
                raise NoPrivateMessage()

            a = cast(User, ctx.author)  # so its a user not member idk

            original = has_permissions(**perms).predicate
            if (
                ctx.author.guild_permissions.administrator
                or await ctx.bot.is_owner(a)
                or await original(ctx)
            ):
                return True
            else:
                raise MissingPermissions(list(perms.keys()))

        return func(extended_check)

    return decorator


admin_owner_perms = admin_owner_perms_p(check)
admin_owner_perms_a = admin_owner_perms_p(app_check)


def bot_admin_perms_p(func: Callable[[Callable], Any]):
    def decorator(**perms: bool):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.me, ClientUser):
                raise NoPrivateMessage()

            original = bot_has_permissions(**perms).predicate

            if ctx.me.guild_permissions.administrator or await original(ctx):
                return True
            else:
                raise BotMissingPermissions(list(perms.keys()))

        return func(extended_check)

    return decorator


bot_admin_perms = bot_admin_perms_p(check)
bot_admin_perms_a = bot_admin_perms_p(app_check)


def admin_owner_guild_perms_p(func: Callable[[Callable], Any]):
    def decorator(**perms: bool):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.author, User):
                raise NoPrivateMessage()

            original = has_guild_permissions(**perms).predicate
            a = cast(User, ctx.author)  # so its a user not member idk

            if (
                await ctx.bot.is_owner(a)
                or ctx.author.guild_permissions.administrator
                or await original(ctx)
            ):
                return True
            else:
                raise MissingPermissions(list(perms.keys()))

        return func(extended_check)

    return decorator


admin_owner_guild_perms = admin_owner_guild_perms_p(check)
admin_owner_guild_perms_a = admin_owner_guild_perms_p(app_check)


def bot_admin_guild_perms_p(func: Callable[[Callable], Any]):
    def decorator(**perms: bool):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.author, User):
                raise NoPrivateMessage()

            original = bot_has_guild_permissions(**perms).predicate
            a = cast(User, ctx.author)  # so its a user not member idk

            if (
                await ctx.bot.is_owner(a)
                or ctx.author.guild_permissions.administrator
                or await original(ctx)
            ):
                return True
            else:
                raise MissingPermissions(list(perms.keys()))

        return func(extended_check)

    return decorator


bot_admin_guild_perms = bot_admin_guild_perms_p(check)
bot_admin_guild_perms_a = bot_admin_guild_perms_p(app_check)


def admin_owner_or_channel_perms_p(func: Callable[[Callable], Any]):
    def decorator(channel: str, **perms: bool):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.author, User):
                raise NoPrivateMessage()

            c = cast(Context, Context)
            ch = await GuildChannelConverter().convert(c, channel)
            permissions = ch.permissions_for(ctx.author)

            missing = [
                perm
                for perm, value in perms.items()
                if getattr(permissions, perm) != value
            ]
            a = cast(User, ctx.author)  # so its a user not member idk

            if await ctx.bot.is_owner(a) or permissions.administrator or not missing:
                return True
            else:
                raise MissingPermissions(missing)

        return func(extended_check)

    return decorator


admin_owner_or_channel_perms = admin_owner_or_channel_perms_p(check)
admin_owner_or_channel_perms_a = admin_owner_or_channel_perms_p(app_check)


def bot_admin_or_channel_perms_p(func: Callable[[Callable], Any]):
    def decorator(channel: str, **perms):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.me, ClientUser):
                raise NoPrivateMessage()

            c = cast(Context, Context)
            ch = await GuildChannelConverter().convert(c, channel)
            permissions = ch.permissions_for(ctx.me)

            missing = [
                perm
                for perm, value in perms.items()
                if getattr(permissions, perm) != value
            ]

            if permissions.administrator or not missing:
                return True
            else:
                raise BotMissingPermissions(missing)

        return func(extended_check)

    return decorator


bot_admin_or_channel_perms = bot_admin_or_channel_perms_p(check)
bot_admin_or_channel_perms_a = bot_admin_or_channel_perms_p(app_check)


def admin_owner_or_arg_perms_p(func: Callable[[Callable], Any]):
    def decorator(arg: int, **perms: bool):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None:
                raise NoPrivateMessage()

            ch = ctx.args[arg]
            permissions = ch.permissions_for(ctx.author)

            missing = [
                perm
                for perm, value in perms.items()
                if getattr(permissions, perm) != value
            ]
            a = cast(User, ctx.author)  # so its a user not member idk

            if await ctx.bot.is_owner(a) or permissions.administrator or not missing:
                return True
            else:
                raise MissingPermissions(missing)

        return func(extended_check)

    return decorator


admin_owner_or_arg_perms = admin_owner_or_arg_perms_p(check)
admin_owner_or_arg_perms_a = admin_owner_or_arg_perms_p(app_check)


def bot_admin_or_arg_perms_p(func: Callable[[Callable], Any]):
    def decorator(arg: int, **perms):
        async def extended_check(ctx: MyContext | MyInter) -> bool:
            if ctx.guild is None or isinstance(ctx.me, ClientUser):
                raise NoPrivateMessage()

            ch = ctx.args[arg]
            permissions = ch.permissions_for(ctx.me)

            missing = [
                perm
                for perm, value in perms.items()
                if getattr(permissions, perm) != value
            ]

            if permissions.administrator or not missing:
                return True
            else:
                raise BotMissingPermissions(missing)

        return func(extended_check)

    return decorator


bot_admin_or_arg_perms = bot_admin_or_arg_perms_p(check)
bot_admin_or_arg_perms_a = bot_admin_or_arg_perms_p(app_check)
