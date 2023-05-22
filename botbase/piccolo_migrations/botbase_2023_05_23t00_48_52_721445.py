from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.table import Table


ID = "2023-05-23T00:48:52:721445"
VERSION = "0.111.1"
DESCRIPTION = "Add UNIQUE to CommandLog"


async def forwards():
    manager = MigrationManager(migration_id=ID, app_name="", description=DESCRIPTION)

    async def composite_unique() -> None:
        class RawTable(Table):
            ...

        await RawTable.raw(
            "ALTER TABLE command_log ADD UNIQUE (command, guild, channel, member);"
        )

    manager.add_raw(composite_unique)

    return manager
