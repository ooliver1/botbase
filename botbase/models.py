from typing import Generic, TypeVar

from nextcord.ext.commands import Cog

from .botbase import BotBase

BotBaseT = TypeVar("BotBaseT", bound=BotBase)
__all__ = ("CogBase",)


class CogBase(Cog, Generic[BotBaseT]):
    def __init__(self, bot: BotBaseT):
        self.bot: BotBaseT = bot
