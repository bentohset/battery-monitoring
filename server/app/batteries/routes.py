from flask import jsonify, current_app
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from app.batteries import battery_bp
from app.extensions import db
from app.common import status

from app.models.battery import Battery
from app.models.timeseriesdata import TimeSeriesData

## get all battery
@battery_bp.route("/", methods = ["GET"])
def get_all_data():
    """
    Retrieves list of all batteries
    
    Returns:
        list: A list of battery objects with fields id, shelf_id and container_id

    """

    batteries = Battery.query.all()

    result = []
    for battery in batteries:
        result.append({
            'id': battery.id,
            'shelf': battery.shelf_id,
            'container': battery.container_id
        })

    return jsonify(result), status.HTTP_200_OK


# gets data of battery with battery id, returns array of readings sorted by time ascending
@battery_bp.route("/<battery_id>", methods = ["GET"])
def get_by_id(battery_id):
    """
    Retrieves timeseriesdata for a specific battery by ID
    
    Fetches data from readings table based on the battery id and returns an array of objects

    Args:
        battery_id (int): ID of the battery which acts as the foregin key

    Returns:
        array: list of objects containing battery readings ordered by time ascending

    Raises:
        404 Not Found: When battery_id provided does not exist within the database
    """
    data = TimeSeriesData.query.filter_by(battery_id=battery_id).order_by(TimeSeriesData.timestamp.asc()).all()

    if not data:
        return jsonify({"message":"Battery with {battery_id} not found"}), status.HTTP_404_NOT_FOUND

    # get over time
    result = []
    for entry in data:
        result.append({
            'timestamp': entry.timestamp,
            'ble_uuid': entry.ble_uuid,
            'humidity': entry.humidity,
            'temperature': entry.temperature,
            'internal_series_resistance': entry.internal_series_resistance,
            'internal_impedance': entry.internal_impedance
        })

    return jsonify(result), status.HTTP_200_OK


## get current data / latest data for each battery
@battery_bp.route("/table", methods = ["GET"])
def get_recent():
    """
    Retrieve all latest battery data unique by battery ID

    Gets latest data for each unique battery ID and sorts it by battery id ascending
    
    Returns:
        array: an array of unique objects of latest battery data ordered by battery_id
    
    """
    result = []
    b = aliased(Battery, name='b')
    r = aliased(TimeSeriesData, name='r')

    latest_subquery = db.session.query(
        r.battery_id,
        func.max(r.timestamp).label('latest_timestamp')
    ).group_by(r.battery_id).subquery()

    readings = db.session.query(
        r,
        b.shelf_id,
        b.container_id
    ).join(
        latest_subquery,
        db.and_(r.battery_id == latest_subquery.c.battery_id, r.timestamp == latest_subquery.c.latest_timestamp)
    ).join(b).all()

    for entry in readings:
        result.append({
            'battery_id': entry.r.battery_id,
            'timestamp': entry.r.timestamp,
            'shelf': entry.shelf_id,
            'container': entry.container_id,
            'ble_uuid': entry.r.ble_uuid,
            'humidity': entry.r.humidity,
            'temperature': entry.r.temperature,
            'internal_series_resistance': entry.r.internal_series_resistance,
            'internal_impedance': entry.r.internal_impedance
        })
    def get_id(elem):
        return elem['battery_id']

    sorted_result = sorted(result, key=get_id)
    
    return jsonify(sorted_result), status.HTTP_200_OK

