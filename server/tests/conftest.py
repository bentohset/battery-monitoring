import pytest
import os
from app import create_app
from config import TestingConfig
from app.models.user import User
from app.models.battery import Battery
from app.models.timeseriesdata import TimeSeriesData
from app.extensions import db

@pytest.fixture(scope='module')
def client():
    os.environ["FLASK_ENV"] = 'testing'
    app = create_app()
    print("testing", app.config['TESTING'])
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def new_user():
    user = User('fixture@gmail.com', 'fixtureTest')
    return user

@pytest.fixture(scope='module')
def init_db(client):
    # create db and tables
    with client.application.app_context():
        db.create_all()

        # insert user
        default_user = User(email='test@gmail.com', password_str='testest')
        second_user = User(email='test2@gmail.com', password_str='testest2')
        db.session.add(default_user)
        db.session.add(second_user)

        db.session.commit()

        battery1 = Battery(1,1)
        battery2 = Battery(1,2)
        battery3 = Battery(2,1)
        battery4 = Battery(2,2)
        db.session.add(battery1)
        db.session.add(battery2)
        db.session.add(battery3)
        db.session.add(battery4)

        db.session.commit()

        data1 = TimeSeriesData(1, 'test1', 11.1111, 22.2222, 33.3333, 44.4444, '6/7/23 17:09:00')
        data2 = TimeSeriesData(2, 'test1', 21.1111, 32.2222, 43.3333, 14.4444, '6/7/23 17:09:00')
        data3 = TimeSeriesData(3, 'test2', 31.1111, 42.2222, 13.3333, 24.4444, '6/7/23 17:09:00')
        data4 = TimeSeriesData(4, 'test2', 41.1111, 12.2222, 23.3333, 34.4444, '6/7/23 17:09:00')
        db.session.add(data1)
        db.session.add(data2)
        db.session.add(data3)
        db.session.add(data4)

        db.session.commit()

        yield

        db.drop_all()

@pytest.fixture(scope='module')
def login_default_user(client):
    client.post('')

    yield

    client.get('')

