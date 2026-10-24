import copy

import pytest

import server


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr(server, 'clubs', copy.deepcopy(server.loadClubs()))
    monkeypatch.setattr(
        server, 'competitions', copy.deepcopy(server.loadCompetitions())
    )
    if hasattr(server, 'bookings'):
        monkeypatch.setattr(server, 'bookings', {})
    server.app.config.update(TESTING=True, SECRET_KEY='test-secret')
    yield server.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def login(client):
    def _login(email='john@simplylift.co'):
        return client.post('/showSummary', data={'email': email})

    return _login
