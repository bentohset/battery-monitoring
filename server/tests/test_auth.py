from app.common import status
from flask import json
from conftest import client, init_db
from app.models.battery import Battery
from app.models.timeseriesdata import TimeSeriesData

BASE_URL = "/auth"

def test_login_success(client, init_db):
    """
    Test login route success
    Given a user that exists within the DB and a valid password

    Should return login success 200 OK
    """

    user = {
        'email': 'test@gmail.com',
        'password': 'testest'
    }

    response = client.post(
        f"{BASE_URL}/login",
        json=user
    )
    data = response.get_json()
    print(data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.get_json()
    assert 'token' in data
    
def test_login_invalid_email(client, init_db):
    """
    Test login route invalid
    Given an invalid email that doesnt exist in the DB

    Shoud return unsuccessful 404 not found
    """

    user = {
        'email': 'te@gmail.com',
        'password': 'testest'
    }

    response = client.post(
        f"{BASE_URL}/login",
        json=user
    )
    data = response.get_json()
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_login_invalid_password(client, init_db):
    """
    Test login route invalid password
    Given a valid email that exist within the DB but an invalid password

    Should always return 401 unauthorized
    """

    user = {
        'email': 'test@gmail.com',
        'password': 'tes'
    }

    response = client.post(
        f"{BASE_URL}/login",
        json=user
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_register_success(client):
    """
    Test register route success
    Given an email and password

    Should return 201 created
    """

    user = {
        'email': 'test3@gmail.com',
        'password': 'tes'
    }
    response = client.post(
        f"{BASE_URL}/register",
        json=user
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.get_json()
    assert 'token' in data


def test_register_user_exists(client, init_db):
    """
    Test register route unsuccessful
    Given an email that already exists within the DB

    Should return 409 conflict
    """
    
    user = {
        'email': 'test@gmail.com',
        'password': 'tes'
    }
    response = client.post(
        f"{BASE_URL}/register",
        json=user
    )

    assert response.status_code == status.HTTP_409_CONFLICT


def test_submit_email(client, init_db):
    pass

def test_submit_invalid_email(client, init_db):
    pass

def test_get_reset_token(client, init_db):
    pass

def test_get_reset_invalid_token(client, init_db):
    pass

def test_get_reset_token_not_requested(client, init_db):
    pass

def update_password(client, init_db):
    pass

def update_password_invalid_token(client, init_db):
    pass

def update_password_not_requested(client, init_db):
    pass
