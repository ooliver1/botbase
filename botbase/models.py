from typing import Generic, TypeVar

from nextcord.ext.commands import Cog

from .botbase import BotBase

B = TypeVar("B", bound=BotBase)
__all__: tuple[str, ...] = ("CogBase",)


class CogBase(Cog, Generic[B]):
    def __init__(self, bot: B):
        self.bot = bot
