from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import abc
from nextcord.ext.commands import TextChannelConverter

from . import wrap

if TYPE_CHECKING:
    from typing import Union


class WrappedChannel(wrap.Wrap, abc.GuildChannel, abc.PrivateChannel):  # type: ignore
    @classmethod
    async def convert(cls, ctx, argument: str) -> WrappedChannel:
        channel: Union[
            abc.GuildChannel, abc.PrivateChannel
        ] = await TextChannelConverter().convert(ctx=ctx, argument=argument)
        return cls(channel, ctx.bot)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
