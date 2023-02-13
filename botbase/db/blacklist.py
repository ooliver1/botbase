from ormar import BigInteger, Model, String

from .metadata import BaseMeta


__all__ = ("BlacklistGuild", "BlacklistUser")


class BlacklistGuild(Model):
    class Meta(BaseMeta):
        tablename = "blacklist_guilds"

    # pyright: reportGeneralTypeIssues=false
    id: int = BigInteger(primary_key=True, autoincrement=False)
    reason: str = String(max_length=255, default="Unknown reason.")


class BlacklistUser(Model):
    class Meta(BaseMeta):
        tablename = "blacklist_users"

    id: int = BigInteger(primary_key=True, autoincrement=False)
    reason: str = String(max_length=255, default="Unknown reason.")
