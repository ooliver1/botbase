# from __future__ import annotations

# from typing import TypeVar, Callable, Union, Coroutine, Any, cast
# from asyncio import iscoroutinefunction
# from functools import wraps

# from nextcord.ext.commands import (
#     BotMissingPermissions,
#     Context,
#     GuildChannelConverter,
#     MissingPermissions,
#     NoPrivateMessage,
#     bot_has_guild_permissions,
#     bot_has_permissions,
#     has_guild_permissions,
#     has_permissions,
#     Command,
# )
# from nextcord import ClientUser, User, Interaction, BaseApplicationCommand

# from .wraps.context import MyContext
# from .wraps.inter import MyInter

# __all__ = (
#     "admin_owner_perms",
#     "bot_admin_perms",
#     "admin_owner_guild_perms",
#     "bot_admin_guild_perms",
#     "admin_owner_or_channel_perms",
#     "bot_admin_or_channel_perms",
#     "admin_owner_or_arg_perms",
#     "bot_admin_or_arg_perms",
# )


# T = TypeVar("T")
# Coro = Coroutine[Any, Any, T]
# CoroFunc = Callable[..., Coro[Any]]
# MaybeCoro = Union[T, Coro[T]]
# CT = TypeVar("CT", bound=Union[Interaction, Context])
# CH = TypeVar("CH", BaseApplicationCommand, Command, CoroFunc)


# # im so sorry if you see this
# def check(predicate) -> Callable[[CH], CH]:
#     def decorator(func: CH) -> CH:
#         if isinstance(func, (BaseApplicationCommand, Command)):
#             func.checks.append(predicate)
#         else:
#             f = cast(CoroFunc, func)
#             if not hasattr(f, "__slash_command_checks__"):
#                 f.__slash_command_checks__ = []

#             if not hasattr(f, "__commands_checks__"):
#                 f.__commands_checks__ = []

#             f.__slash_command_checks__.append(predicate)
#             f.__commands_checks__.append(predicate)

#         return func

#     if iscoroutinefunction(predicate):
#         decorator.predicate = predicate
#     else:

#         @wraps(predicate)
#         async def wrapper(h):
#             return predicate(h)

#         decorator.predicate = wrapper

#     return decorator


# def admin_owner_perms(**perms: bool):
#     """user has admin or is me or permissions"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.author, User):
#             raise NoPrivateMessage()

#         a = cast(User, ctx.author)  # so its a user not member idk

#         original = has_permissions(**perms).predicate
#         if (
#             ctx.author.guild_permissions.administrator
#             or await ctx.bot.is_owner(a)
#             or await original(ctx)
#         ):
#             return True
#         else:
#             raise MissingPermissions(list(perms.keys()))

#     return check(extended_check)


# def bot_admin_perms(**perms: bool):
#     """bot is admin or has perms (channel based)"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.me, ClientUser):
#             raise NoPrivateMessage()

#         original = bot_has_permissions(**perms).predicate

#         if ctx.me.guild_permissions.administrator or await original(ctx):
#             return True
#         else:
#             raise BotMissingPermissions(list(perms.keys()))

#     return check(extended_check)


# def admin_owner_guild_perms(**perms: bool):
#     """user is admin or me or permissions (guild based)"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.author, User):
#             raise NoPrivateMessage()

#         original = has_guild_permissions(**perms).predicate
#         a = cast(User, ctx.author)  # so its a user not member idk

#         if (
#             await ctx.bot.is_owner(a)
#             or ctx.author.guild_permissions.administrator
#             or await original(ctx)
#         ):
#             return True
#         else:
#             raise MissingPermissions(list(perms.keys()))

#     return check(extended_check)


# def bot_admin_guild_perms(**perms: bool):
#     """bot is admin or perms (guild based)"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.author, User):
#             raise NoPrivateMessage()

#         original = bot_has_guild_permissions(**perms).predicate
#         a = cast(User, ctx.author)  # so its a user not member idk

#         if (
#             await ctx.bot.is_owner(a)
#             or ctx.author.guild_permissions.administrator
#             or await original(ctx)
#         ):
#             return True
#         else:
#             raise MissingPermissions(list(perms.keys()))

#     return check(extended_check)


# def admin_owner_or_channel_perms(channel: str, **perms: bool):
#     """user is admin or me or has perms on channel"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.author, User):
#             raise NoPrivateMessage()

#         c = cast(Context, Context)
#         ch = await GuildChannelConverter().convert(c, channel)
#         permissions = ch.permissions_for(ctx.author)

#         missing = [
#             perm for perm, value in perms.items() if getattr(permissions, perm) != value
#         ]
#         a = cast(User, ctx.author)  # so its a user not member idk

#         if await ctx.bot.is_owner(a) or permissions.administrator or not missing:
#             return True
#         else:
#             raise MissingPermissions(missing)

#     return check(extended_check)


# def bot_admin_or_channel_perms(channel: str, **perms):
#     """bot is admin or has perms on channel"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.me, ClientUser):
#             raise NoPrivateMessage()

#         c = cast(Context, Context)
#         ch = await GuildChannelConverter().convert(c, channel)
#         permissions = ch.permissions_for(ctx.me)

#         missing = [
#             perm for perm, value in perms.items() if getattr(permissions, perm) != value
#         ]

#         if permissions.administrator or not missing:
#             return True
#         else:
#             raise BotMissingPermissions(missing)

#     return check(extended_check)


# def admin_owner_or_arg_perms(arg: int, **perms: bool):
#     """user is admin or me or has perms on channel"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None:
#             raise NoPrivateMessage()

#         ch = ctx.args[arg]
#         permissions = ch.permissions_for(ctx.author)

#         missing = [
#             perm for perm, value in perms.items() if getattr(permissions, perm) != value
#         ]
#         a = cast(User, ctx.author)  # so its a user not member idk

#         if await ctx.bot.is_owner(a) or permissions.administrator or not missing:
#             return True
#         else:
#             raise MissingPermissions(missing)

#     return check(extended_check)


# def bot_admin_or_arg_perms(arg: int, **perms):
#     """bot is admin or has perms on channel"""

#     async def extended_check(ctx: MyContext | MyInter) -> bool:
#         if ctx.guild is None or isinstance(ctx.me, ClientUser):
#             raise NoPrivateMessage()

#         ch = ctx.args[arg]
#         permissions = ch.permissions_for(ctx.me)

#         missing = [
#             perm for perm, value in perms.items() if getattr(permissions, perm) != value
#         ]

#         if permissions.administrator or not missing:
#             return True
#         else:
#             raise BotMissingPermissions(missing)

#     return check(extended_check)
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME: imple# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME
# FIXME: implement for the new slash checks api
