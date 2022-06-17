from __future__ import annotations

from typing import TYPE_CHECKING

from nextcord import (
    Message,
    Embed,
    WebhookMessage,
    TextChannel,
    Thread,
    DMChannel,
    PartialMessageable,
)
from nextcord.abc import Messageable
from nextcord.utils import utcnow
from nextcord.embeds import _EmptyEmbed

if TYPE_CHECKING:
    from typing import Any

    from ..botbase import BotBase


channels = (TextChannel, PartialMessageable, Thread, DMChannel, Messageable)


class Wrap:
    def __init__(self, wrapped, bot: BotBase):
        self._wrapped = wrapped
        self._bot = bot

        if isinstance(wrapped, type(self)):
            self._wrapped = wrapped._wrapped

    def __instancecheck__(self, instance: Any):
        return isinstance(instance, type(self._wrapped))

    def __subclasscheck__(self, subclass: Any):
        return issubclass(subclass, self._wrapped)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, (type(self._wrapped), type(self))):
            return False

        if isinstance(other, type(self._wrapped)):
            return other.id == self._wrapped.id

        return other._wrapped.id == self._wrapped.id

    def __hash__(self):
        return hash(self._wrapped)

    async def send_author_embed(self, text: str, **kwargs):
        return await self.send_embed(
            author=text,
            cmd_invoker=False,
            invoker_in_author=True,
            try_channel=True,
            **kwargs,
        )

    async def send_embed(
        self,
        title: str | _EmptyEmbed = Embed.Empty,
        desc: str | _EmptyEmbed = Embed.Empty,
        *,
        author: str | None = None,
        image: str | None = None,
        thumbnail: str | None = None,
        color=None,
        target=None,
        reply: bool = False,
        contain_timestamp: bool = True,
        cmd_invoker: bool = True,
        invoker_in_author: bool = False,
        try_channel: bool = False,
        **kwargs,
    ) -> Message | WebhookMessage | None:
        from .context import MyContext
        from .channel import WrappedChannel
        from .inter import MyInter
        from .thread import WrappedThread
        from .member import WrappedMember
        from .user import WrappedUser

        target = target or (
            self.message  # ctx, reply=True
            if reply and isinstance(self, MyContext)
            else self  # Anything else (member.send)
        )

        embed = Embed(title=title, description=desc, color=color or self._bot.color)

        if contain_timestamp and isinstance(self, MyContext):
            # Doesnt work on Channels, Users, Members
            embed.timestamp = self.message.created_at
        elif contain_timestamp:
            embed.timestamp = utcnow()

        if cmd_invoker and not isinstance(self, (WrappedChannel, WrappedThread)):
            if isinstance(self, (MyContext)):
                text = self.author.display_name
                icon_url = self.author.display_avatar.url
            elif isinstance(self, MyInter):
                text = self.user.display_name
                icon_url = self.user.display_avatar.url
            elif isinstance(self, (WrappedUser, WrappedMember)):
                text = self.display_name
                icon_url = self.display_avatar.url
            else:
                raise TypeError(f"{type(self).__name__} cannot get invoker")

            embed.set_footer(text=text, icon_url=icon_url)

        if author:
            if isinstance(self, (MyContext)):
                icon_url = self.author.display_avatar.url
            elif isinstance(self, MyInter):
                icon_url = self.user.display_avatar.url
            elif isinstance(self, (WrappedUser, WrappedMember)):
                icon_url = self.display_avatar.url
            else:
                raise TypeError(f"{type(self).__name__} cannot get invoker")

            if invoker_in_author:
                embed.set_author(name=author, icon_url=icon_url)
            else:
                embed.set_author(name=author)

        if image:
            embed.set_image(url=image)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if reply and isinstance(target, Message):
            return await target.reply(embed=embed, **kwargs)
        elif isinstance(target, Message):
            return await target.channel.send(embed=embed, **kwargs)
        elif try_channel and isinstance(target, MyInter) and target.response.is_done():
            if isinstance(target.channel, channels):
                return await target.channel.send(embed=embed, **kwargs)
            else:
                return await target.send(embed=embed, **kwargs)  # type: ignore
        elif isinstance(
            target,
            (
                WrappedUser,
                WrappedMember,
                WrappedChannel,
                WrappedThread,
                MyInter,
                MyContext,
            ),
        ):
            return await target.send(embed=embed, **kwargs)  # type: ignore
        else:
            raise TypeError(f"{type(self).__name__} cannot send embeds")
