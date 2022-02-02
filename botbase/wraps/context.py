from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord.ext.commands import Context

from . import wrap.Wrap

if TYPE_CHECKING:
    from ..botbase import BotBase


class MyContext(Context, wrap.Wrap):
    bot: BotBase

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = self.bot.get_wrapped_message(self.message)
        self.author = self.bot.get_wrapped_person(self.author)
        self.channel = self.bot.get_wrapped_channel(self.channel)
