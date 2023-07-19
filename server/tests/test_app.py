from app.common import status
from conftest import client

def test_status_ok(client):
    """
    Test route
    Always returns 200 OK
    """
    
    response = client.get('/test')
    assert response.status_code == status.HTTP_200_OK

def test_status_health(client):
    """
    Tests the health status of the server

    Should always return 200 OK
    """

    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    
    data = response.get_json()
    print(data)
    assert data["status"] == "OK"