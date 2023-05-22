import asyncio
from functools import partial

from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import BigInt, Integer, Text
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table

ID = "2023-05-23T00:19:45:350876"
VERSION = "0.111.1"
DESCRIPTION = "Add initial tables"


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="botbase", description=DESCRIPTION
    )

    manager.add_table("BlacklistGuild", tablename="blacklist_guild")

    manager.add_table("BlacklistUser", tablename="blacklist_user")

    manager.add_table("CommandLog", tablename="command_log")

    manager.add_column(
        table_class_name="BlacklistGuild",
        tablename="blacklist_guild",
        column_name="id",
        db_column_name="id",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="BlacklistGuild",
        tablename="blacklist_guild",
        column_name="reason",
        db_column_name="reason",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "Unknown reason.",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="BlacklistUser",
        tablename="blacklist_user",
        column_name="id",
        db_column_name="id",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="BlacklistUser",
        tablename="blacklist_user",
        column_name="reason",
        db_column_name="reason",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "Unknown reason.",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CommandLog",
        tablename="command_log",
        column_name="command",
        db_column_name="command",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CommandLog",
        tablename="command_log",
        column_name="guild",
        db_column_name="guild",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CommandLog",
        tablename="command_log",
        column_name="channel",
        db_column_name="channel",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CommandLog",
        tablename="command_log",
        column_name="member",
        db_column_name="member",
        column_class_name="BigInt",
        column_class=BigInt,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="CommandLog",
        tablename="command_log",
        column_name="amount",
        db_column_name="amount",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 1,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    async def composite_unique() -> None:
        class RawTable(Table):
            ...

        for _ in range(100):
            try:
                await RawTable.raw(
                    "ALTER TABLE command_log "
                    "ADD UNIQUE (command, guild, channel, member);"
                )
            except Exception:
                await asyncio.sleep(0.1)

    manager.add_raw(partial(asyncio.create_task, composite_unique()))

    return manager
