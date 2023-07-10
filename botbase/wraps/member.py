from __future__ import annotations

from nextcord import Member

from . import wrap


class WrappedMember(wrap.Wrap, Member):
    def __getattr__(self, item):
        return getattr(self._wrapped, item)
