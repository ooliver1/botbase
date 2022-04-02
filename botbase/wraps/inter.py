from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import Interaction, InteractionResponse

from . import wrap

if TYPE_CHECKING:
    from nextcord import VoiceProtocol, ClientUser, Member

    from ..botbase import BotBase
    from .user import WrappedUser
    from .member import WrappedMember


class MyInter(wrap.Wrap, Interaction):
    user: WrappedUser | WrappedMember
    author: WrappedUser | WrappedMember
    prefix = "/"
    clean_prefix = "/"

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
    def command(self) -> str | None:
        if self.data:
            return self.data.get("name")

    @property  # maybe this is why it no worky
    def response(self) -> InteractionResponse:
        return self._wrapped.response

    def __getattr__(self, item):
        return getattr(self._wrapped, item)
