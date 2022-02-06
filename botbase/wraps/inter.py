from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import Interaction

from . import wrap

if TYPE_CHECKING:
    from ..botbase import BotBase


class MyInter(Interaction, wrap.Wrap):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = self.bot.get_wrapped_person(self.user)

    @property
    def _bot(self) -> BotBase:
        return self.client  # type: ignore

    def bot(self) -> BotBase:
        return self.client  # type: ignore
