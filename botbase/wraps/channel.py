from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import abc, Permissions, DMChannel
from nextcord.ext.commands import TextChannelConverter

from . import wrap

if TYPE_CHECKING:
    from typing import Union


class WrappedChannel(wrap.Wrap, abc.GuildChannel, abc.PrivateChannel):  # type: ignore
    def __getattr__(self, item):
        return getattr(self._wrapped, item)

    def permissions_for(self, *args, **kwargs):
        if not hasattr(self, "guild"):
            return Permissions.all()

        return super().permissions_for(*args, **kwargs)
