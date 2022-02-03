from __future__ import annotations

from nextcord import User
from nextcord.ext.commands import UserConverter

from . import wrap


class WrappedUser(wrap.Wrap, User):
    @classmethod
    async def convert(cls, ctx, argument: str) -> WrappedUser:
        user: User = await UserConverter().convert(
            ctx=ctx, argument=argument
        )
        return cls(user, ctx.bot)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
