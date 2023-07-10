from __future__ import annotations

from nextcord import Thread

from . import wrap


class WrappedThread(wrap.Wrap, Thread):
    def __getattr__(self, item):
        return getattr(self._wrapped, item)
