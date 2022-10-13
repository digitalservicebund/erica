from erica.worker.huey import eric_wrapper_init, get_initialised_eric_wrapper, shutdown_eric_wrapper


class TestEricWrapperInitialize:

    def test_if_eric_wrapper_initialized_get_init_eric_wrapper_returns_not_none(self):
        eric_wrapper_init()
        try:
            assert get_initialised_eric_wrapper() is not None
        finally:
            shutdown_eric_wrapper()
