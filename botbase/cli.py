from sys import argv
from asyncio import run

from asyncpg import create_pool


async def init(url: str):
    pool = await create_pool(url)

    await pool.execute(
        """
        CREATE TABLE IF NOT EXISTS blacklist_users (
            id BIGINT PRIMARY KEY,
            reason VARCHAR NOT NULL
        );
        CREATE TABLE IF NOT EXISTS blacklist_guilds (
            id BIGINT PRIMARY KEY,
            reason VARCHAR NOT NULL
        );
        CREATE TABLE IF NOT EXISTS guilds (
            id BIGINT PRIMARY KEY,
            prefix VARCHAR
        );
        CREATE TABLE IF NOT EXISTS commands (
            command VARCHAR NOT NULL,
            guild BIGINT,
            channel BIGINT,
            member BIGINT NOT NULL,
            amount INT NOT NULL
        );
    """
    )


def main():
    if len(argv) == 1:
        print("Usage: botbase <url>")

    run(init(argv[1]))
