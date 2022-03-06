import os

from opyoid import Provider
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.infrastructure.sqlalchemy.tax_declaration import TaxDeclarationEntity
from src.infrastructure.sqlalchemy.freischalt_code import FreischaltCodeEntity
from src.infrastructure.sqlalchemy.freischalt_code_activate import FreischaltCodeActivateEntity
from src.infrastructure.sqlalchemy.freischalt_code_revocate import FreischaltCodeRevocateEntity

DATABASE_URL = 'postgresql://postgres:postgres@localhost/db'

uri = DATABASE_URL or os.getenv('DB_URI')
engine = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url)
else:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migrations():
    __create_tables_if_not_exists()


def __create_tables_if_not_exists():
    # NOTE:  use Alembic for migrations (https://alembic.sqlalchemy.org/en/latest/)
    TaxDeclarationEntity.metadata.create_all(bind=engine)
    FreischaltCodeEntity.metadata.create_all(bind=engine)
    FreischaltCodeActivateEntity.metadata.create_all(bind=engine)
    FreischaltCodeRevocateEntity.metadata.create_all(bind=engine)


class DbSession(Session):
    pass


class DatabaseSessionProvider(Provider[DbSession]):
    def get(self) -> DbSession:
        return SessionLocal()
