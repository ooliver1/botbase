from __future__ import annotations

from nextcord import User
from nextcord.ext.commands import UserConverter

from . import wrap


class WrappedUser(wrap.Wrap, User):
    def __getattr__(self, item):
        return getattr(self._wrapped, item)
