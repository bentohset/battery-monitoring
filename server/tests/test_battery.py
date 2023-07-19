from app.common import status
from conftest import client, init_db
from app.models.battery import Battery
from app.models.timeseriesdata import TimeSeriesData

BASE_URL = "/battery"

def test_get_all_battery(client, init_db):
    """
    Test get all battery routes
    Given a prepopulated DB with battery info

    Should return a list of 4 objects and 200 OK
    """

    response = client.get(
        f"{BASE_URL}/"
    )
    assert response.status_code == status.HTTP_200_OK
    
    data =  response.get_json()

    assert len(data) == 4


def test_get_battery_id(client, init_db):
    """
    Test get battery reading by id route success
    Given a valid battery id and a prepopulated DB with one reading per battery

    Should return an array of objects relating to battery readings
    """

    response = client.get(
        f"{BASE_URL}/1"
    )
    assert response.status_code == status.HTTP_200_OK
    
    data = response.get_json()

    assert len(data) == 2
    assert data[0]['temperature'] == 22.2222
    assert data[0]['ble_uuid'] == 'test1'


def test_battery_not_found(client, init_db):
    """
    Test get battery reading by id invalid id
    Given an invalid battery id which does not exist within the DB

    Should return 404 not found
    """

    response = client.get(
        f"{BASE_URL}/0"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_latest_data(client, init_db):
    """Test get latest data for each battery route
    Given a prepopulated DB with 2 readings per data

    Returns an array of objects relating to latest battery readings of all batteries
    """
    
    response = client.get(
        f"{BASE_URL}/table"
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.get_json()

    assert len(data) == 4
    assert data[0]['temperature'] == 33.2222


