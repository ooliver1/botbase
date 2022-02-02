from __future__ import annotations

from nextcord import Thread
from nextcord.ext.commands import ThreadConverter

from . import wrap


class WrappedThread(wrap.Wrap, Thread):
    @classmethod
    async def convert(cls, ctx, argument: str) -> WrappedThread:
        _meta: Thread = await ThreadConverter().convert(ctx=ctx, argument=argument)
        return cls(_meta, ctx.bot)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
