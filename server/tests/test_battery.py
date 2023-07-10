from app.common import status
from conftest import client, init_db
from app.models.battery import Battery
from app.models.timeseriesdata import TimeSeriesData

BASE_URL = "/battery"

def test_get_all_battery(client, init_db):
    response = client.get(
        f"{BASE_URL}/"
    )
    assert response.status_code == status.HTTP_200_OK
    
    data =  response.get_json()

    assert len(data) == 4


def test_battery_not_found(client, init_db):
    response = client.get(
        f"{BASE_URL}/0"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_battery_id(client, init_db):
    response = client.get(
        f"{BASE_URL}/1"
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.get_json()

    assert len(data) == 1
    assert data[0]['temperature'] == 22.2222
    assert data[0]['ble_uuid'] == 'test1'


def test_get_latest_data(client, init_db):
    response = client.get(
        f"{BASE_URL}/table"
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.get_json()

    assert len(data) == 4


