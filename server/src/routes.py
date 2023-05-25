from flask import jsonify, current_app, Blueprint
from sqlalchemy import select, func
from sqlalchemy.orm import aliased

from .models import Battery, TimeSeriesData
from . import db

routes = Blueprint('routes', __name__)

## get all battery
@routes.route("/data", methods = ["GET"])
def get_all_data():
    batteries = Battery.query.all()

    result = []
    for battery in batteries:
        result.append({
            'id': battery.id,
            'shelf': battery.shelf_id,
            'container': battery.container_id
        })

    return jsonify(result), 200

# gets data of battery with battery id, returns array of readings sorted by time ascending
@routes.route("/data/<battery_id>", methods = ["GET"])
def get_by_id(battery_id):
    data = TimeSeriesData.query.filter_by(battery_id=battery_id).order_by(TimeSeriesData.timestamp.asc()).all()

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

    return jsonify(result), 200

## get current data / latest data for each battery
@routes.route("/data/table", methods = ["GET"])
def get_recent():
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

    # query = select(r, b.shelf_id, b.container_id)\
    #     .distinct(r.battery_id)\
    #     .join(b, b.id == r.battery_id)\
    #     .order_by(r.battery_id, r.timestamp.desc())

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
    
    return jsonify(result), 200

