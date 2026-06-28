import types

from fastapi.testclient import TestClient

from app.main import app
from app.startup import configure_app


class DummyRouter:
    def __init__(self):
        self.on_startup = []


class DummyApp:
    def __init__(self):
        self.state = types.SimpleNamespace()
        self.router = DummyRouter()
        self.middleware_stack = []
        self.exception_handlers = {}

    def add_middleware(self, middleware):
        self.middleware_stack.append(middleware)

    def add_exception_handler(self, exc_type, handler):
        self.exception_handlers[exc_type] = handler


def test_configure_app_registers_startup_handler_without_add_event_handler():
    app = DummyApp()

    configure_app(app)

    assert len(app.router.on_startup) == 1
    assert app.router.on_startup[0].__name__ == 'on_startup'


def test_health_check_endpoint(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to RAG Document QA API'}


def test_app_routers_are_loaded(client):
    response = client.get('/report')

    assert response.status_code == 200
