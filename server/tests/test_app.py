from app.common import status
from conftest import client

def test_status_ok(client):
    response = client.get('/test')
    assert response.status_code == status.HTTP_200_OK

def test_status_health(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    
    data = response.get_json()
    print(data)
    assert data["status"] == "OK"