from sys import argv
from asyncio import run

from asyncpg import create_pool


table = """
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
tables = table.split(";")



async def init(url: str):
    pool = await create_pool(url)

    for table in tables:
        await pool.execute(table)

    print("Done!")
    await pool.close()
    exit(0)


def main():
    if len(argv) == 1:
        print("Usage: botbase <url>")
        exit(1)

    run(init(argv[1]))
