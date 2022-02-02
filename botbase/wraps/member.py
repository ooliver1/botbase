from __future__ import annotations

from nextcord import Member
from nextcord.ext.commands import MemberConverter

from . import wrap


class WrappedMember(wrap.Wrap, Member):
    @classmethod
    async def convert(cls, ctx, argument: str) -> WrappedMember:
        member: Member = await MemberConverter().convert(ctx=ctx, argument=argument)
        return cls(member, ctx.bot)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
