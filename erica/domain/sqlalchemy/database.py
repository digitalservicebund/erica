import decimal

import orjson
from fastapi_sqlalchemy import db
from opyoid import Provider
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from erica.config import get_settings


def default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError


def orjson_serializer(obj):
    """
        Note that `orjson.dumps()` return byte array, while sqlalchemy expects string, thus `decode()` call.
    """
    return orjson.dumps(obj, option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NAIVE_UTC, default=default).decode()


def orjson_deserializer(json):
    return orjson.loads(json)


def get_engine():
    return create_engine(
        get_settings().database_url, **engine_args)


class DatabaseSessionProvider(Provider[Session]):

    def get(self) -> Session:
        return db.session


session_scope = db

engine_args = dict(json_serializer=orjson_serializer,
                   json_deserializer=orjson_deserializer,
                   pool_size=30,
                   max_overflow=90,
                   hide_parameters=True)
