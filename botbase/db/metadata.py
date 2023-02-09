from os import environ

from databases import Database
from dotenv import load_dotenv
from ormar import ModelMeta
from sqlalchemy import MetaData

load_dotenv()


__all__ = (
    "database",
    "metadata",
    "BaseMeta",
)

database = Database(environ["DB_URI"])
metadata = MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database
