from piccolo.table import Table
from piccolo.columns import BigInt, Text


__all__ = ("BlacklistGuild", "BlacklistUser")


class BlacklistGuild(Table):
    id = BigInt(primary_key=True)
    reason = Text(default="Unknown reason.")


class BlacklistUser(Table):
    id = BigInt(primary_key=True)
    reason = Text(default="Unknown reason.")
