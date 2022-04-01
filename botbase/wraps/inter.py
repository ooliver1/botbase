from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import Interaction
from nextcord.utils import get

from . import wrap

if TYPE_CHECKING:
    from nextcord import VoiceProtocol, ClientUser, Member, ApplicationCommand

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

    @property
    def bot(self) -> BotBase:
        return self.client  # type: ignore

    @property
    def voice_client(self) -> VoiceProtocol | None:
        return self.guild and self.guild.voice_client

    @property
    def me(self) -> ClientUser | Member:
        return self.guild.me if self.guild is not None else self.bot.user  # type: ignore

    @property
    def command(self) -> ApplicationCommand | None:
        if self.data:
            if name := self.data.get("name"):
                return get(self.bot.get_application_commands(), name=name)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
