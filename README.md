# botbase

This is a botbase project for [nextcord](https://github.com/nextcord/nextcord) Discord Python bots to reduce boilerplate.

## Config values

`db_enabled: bool` default `True`

`db_url: str` either this or name

`db_name: str` either this or url

`db_user: str` default `"ooliver"`

`db_host str` default `"localhost"`

`version: str` default `"0.0.0"`

`aiohttp_enabled: bool` default `True`

`colors: list[int]` default `[0x9966CC]`

`blacklist_enabled: bool` default `True`

`prefix: str | list[str]`

`helpmsg: str` default [`defaulthelpmsg`](https://github.com/ooliver1/botbase/blob/main/botbase/botbase.py#L38-L47)

`helpindex: str` default [`defaulthelpindex`](https://github.com/ooliver1/botbase/blob/main/botbase/botbase.py#L48-L50)

`helptitle: str` default `"Help Me!"`

`helpfields: dict[str, str]` default `{}`

`helpinsert: str` default `""`

`emojiset: Emojis[str, str]` default `Emojis()`

`logchannel: int` default `None`

`guild_ids: list[int]` default `None`
