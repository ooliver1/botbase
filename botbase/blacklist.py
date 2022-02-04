from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncpg import Pool


class Blacklist:
    def __init__(self, db: Pool) -> None:
        self.db = db

        self.guilds = set()
        self.users = set()

    def __contains__(self, obj: int) -> bool:
        assert isinstance(obj, int)

        return obj in self.guilds or obj in self.users

    async def add(
        self, obj: int, reason: str = "Unknown reason", guild: bool = False
    ) -> None:
        assert isinstance(obj, int)

        if guild:
            self.guilds.add(obj)
            await self.db.execute(
                """
                INSERT INTO blacklist_guilds (id, reason)
                VALUES ($1, $2)
                ON CONFLICT (id) DO UPDATE
                    SET reason = $2
            """,
                obj,
                reason,
            )
        else:
            self.users.add(obj)
            await self.db.execute(
                """
                INSERT INTO blacklist_users (id, reason)
                VALUES ($1, $2)
                ON CONFLICT (id) DO UPDATE
                    SET reason = $2
            """,
                obj,
                reason,
            )

    async def remove(self, obj: int, guild: bool = False) -> None:
        assert isinstance(obj, int)

        if guild:
            self.guilds.discard(obj)
            await self.db.execute(
                """
                DELETE FROM blacklist_guilds
                WHERE id = $1
            """,
                obj,
            )
        else:
            self.users.discard(obj)
            await self.db.execute(
                """
                DELETE FROM blacklist_users
                WHERE id = $1
            """,
                obj,
            )
