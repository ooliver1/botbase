# botbase

This is a bot base project for Discord python bots made with [nextcord](https://github.com/nextcord/nextcord) to reduce boilerplate.

## Config values

| Key                 | Type               | Default                                          |
| ------------------- | ------------------ | ------------------------------------------------ |
| `db_enabled`        | `bool`             | `True`                                           |
| `db_url`            | `str`              |                                                  |
| `db_name`           | `str`              |                                                  |
| `db_user`           | `str`              | `"ooliver"`                                      |
| `db_host`           | `str`              | `"localhost"`                                    |
| `version`           | `str`              | `"0.0.0"`                                        |
| `aiohttp_enabled`   | `bool`             | `True`                                           |
| `colors`            | `list[int]`        | `[0x9966CC]`                                     |
| `blacklist_enabled` | `bool`             | `True`                                           |
| `prefix`            | `str \| list[str]` | `None`                                           |
| `helpmsg`           | `str`              | [`defaulthelpmsg`](botbase/botbase.py#L38-L47)   |
| `helpindex`         | `str`              | [`defaulthelpindex`](botbase/botbase.py#L48-L50) |
| `helptitle`         | `str`              | `"Help Me!"`                                     |
| `helpfields`        | `dict[str, str]`   | `{}`                                             |
| `helpinsert`        | `str`              | `""`                                             |
| `emojiset`          | `Emojis[str, str]` | `Emojis[]`                                       |
| `logchannel`        | `int`              | `None`                                           |
| `guild_ids`         | `list[int]`        | `None`                                           |
