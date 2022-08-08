import os
from sys import platform
from functools import lru_cache

from pydantic import Field
from pydantic.env_settings import BaseSettings


class UnknownEricaEnvironment(Exception):
    """ Exception raised in case an unknown environment is set in the ERICA_ENV variable"""

    pass


class Settings(BaseSettings):
    send_file_max_age_default: int = 60
    cert_pin: str = Field("123456", env='CERT_PIN')
    cert_path: str = 'erica/worker/instances/blueprint/cert.pfx'
    using_stick: bool = True
    use_testmerker: bool = True
    accept_test_bufa: bool = False
    abruf_code: str = Field("LD6LC-FSVEU", env='ABRUF_CODE')
    debug: bool = False
    log_eric_debug_info: bool = False
    testing_email_address: str = 'steuerlotse_testing@4germany.org'  # always set, but not evaluated at Elster's
    elster_datenlieferant: str = Field("PLACEHOLDER_DATENLIEFERANT", env='ELSTER_DATENLIEFERANT')
    hersteller_id: str = Field("74931", env='ELSTER_HERSTELLER_ID')
    queue_url: str = Field("redis://default@localhost:6379/0", env='QUEUE_URL')
    default_queue: str = 'dongle'
    database_url: str = Field("postgresql://postgres:postgres@localhost/db", env="ERICA_DATABASE_URL")
    dongle_connected: bool = Field(True, env="DONGLE_CONNECTED")
    ttl_queuing_job_in_sec: int = 60
    ttl_processing_request_entities_in_min: int = 2
    ttl_finished_request_entities_in_min: int = 10
    use_immediate_worker: bool = False
    sentry_dsn_api: str = None
    sentry_dsn_worker: str = None

    class Config:
        dir = os.path.dirname(__file__)
        env_file = os.path.join(dir, '.env')

    @staticmethod
    def get_eric_dll_path():
        if platform == "darwin":
            return "erica/worker/lib/libericapi.dylib"
        else:
            return "erica/worker/lib/libericapi.so"

    def get_cert_path(self):
        if self.using_stick:
            if platform == 'darwin':
                return 'libaetpkss.dylib'
            else:
                return 'libaetpkss.so'
        else:
            return self.cert_path


class ProductionSettings(Settings):
    env_name: str = "production"
    using_stick: bool = True
    use_testmerker: bool = False
    accept_test_bufa: bool = False
    sentry_dsn_api: str = "https://e8cbb2aaeed742c19965960951c7835c@o1248831.ingest.sentry.io/6466521"
    sentry_dsn_worker: str = "https://fe49771e429c48be8deb9074556c5463@o1248831.ingest.sentry.io/6466074"


class StagingSettings(Settings):
    env_name: str = "staging"
    using_stick: bool = True
    accept_test_bufa: bool = True
    sentry_dsn_api: str = "https://e8cbb2aaeed742c19965960951c7835c@o1248831.ingest.sentry.io/6466521"
    sentry_dsn_worker: str = "https://fe49771e429c48be8deb9074556c5463@o1248831.ingest.sentry.io/6466074"


class DevelopmentSettings(Settings):
    env_name: str = "development"
    using_stick: bool = False
    debug: bool = True
    accept_test_bufa: bool = True


class TestingSettings(Settings):
    env_name: str = "testing"
    using_stick: bool = False
    debug: bool = True
    accept_test_bufa: bool = True
    use_immediate_worker: bool = True


@lru_cache()
def get_settings():
    env = os.environ['ERICA_ENV']
    if env == 'development':
        return DevelopmentSettings()
    elif env == 'testing':
        return TestingSettings()
    elif env == 'staging':
        return StagingSettings()
    elif env == 'production':
        return ProductionSettings()
    else:
        raise UnknownEricaEnvironment
