from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from nextcord.ext.commands import Context


from . import wrap

if TYPE_CHECKING:
    from ..botbase import BotBase

B = TypeVar("B", bound="BotBase")


class MyContext(Context, wrap.Wrap, Generic[B]):
    bot: B

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._bot = self.bot

        self.message = self.bot.get_wrapped_message(self.message)
