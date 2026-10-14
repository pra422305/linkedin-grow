import pytest

from app import create_app, db
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register_and_login(client):
    client.post(
        "/auth/register",
        data={"name": "Test User", "email": "test@example.com", "password": "password123"},
        follow_redirects=True,
    )
