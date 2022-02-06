from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import Interaction

from . import wrap

if TYPE_CHECKING:
    from ..botbase import BotBase
    from .user import WrappedUser
    from .member import WrappedMember


class MyInter(wrap.Wrap, Interaction):
    user: WrappedUser | WrappedMember
    author: WrappedUser | WrappedMember

    def __init__(self, wrapped, bot: BotBase):
        self._wrapped = wrapped

        if isinstance(wrapped, type(self)):
            self._wrapped = wrapped._wrapped

    @property
    def _bot(self) -> BotBase:
        return self.client  # type: ignore

    def bot(self) -> BotBase:
        return self.client  # type: ignore

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
