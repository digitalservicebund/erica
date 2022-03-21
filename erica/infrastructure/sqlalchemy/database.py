import orjson
from opyoid import Provider
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from erica.erica_legacy.config import get_settings
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema


def orjson_serializer(obj):
    """
        Note that `orjson.dumps()` return byte array, while sqlalchemy expects string, thus `decode()` call.
    """
    return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC).decode()


def orjson_deserializer(json):
    return orjson.loads(json)


def get_engine():
    return create_engine(get_settings().database_url, json_serializer=orjson_serializer, json_deserializer=orjson_deserializer)


def run_migrations():
    __create_tables_if_not_exists()


def __create_tables_if_not_exists():
    # NOTE:  use Alembic for migrations (https://alembic.sqlalchemy.org/en/latest/)
    EricaRequestSchema.metadata.create_all(bind=get_engine())


class DatabaseSessionProvider(Provider[Session]):

    def get(self) -> Session:
        engine = get_engine()
        if not database_exists(engine.url):
            create_database(engine.url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
