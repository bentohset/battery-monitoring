import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from src import create_app, db
from src.models import User

@pytest.fixture(scope='session')
def app():
    app = create_app('config.TestingConfig')
    return app

@pytest.fixture(scope='session')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_hello_backend(client):
    response = client.get("/data/table")
    print(response.data)
    assert response.status_code == 200
    assert response.get_json() == {'message':'hello backend'}


