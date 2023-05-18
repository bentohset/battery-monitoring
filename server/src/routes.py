from flask import jsonify, current_app, Blueprint
from sqlalchemy import select
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
            'voltage_open_circuit': entry.voltage_open_circuit,
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

    query = select(r, b.shelf_id, b.container_id)\
        .distinct(r.battery_id)\
        .join(b, b.id == r.battery_id)\
        .order_by(r.battery_id, r.timestamp.desc())

    data = db.session.execute(query)

    for entry in data:
        result.append({
            'battery_id': entry.r.battery_id,
            'timestamp': entry.r.timestamp,
            'shelf': entry.shelf_id,
            'container': entry.container_id,
            'ble_uuid': entry.r.ble_uuid,
            'humidity': entry.r.humidity,
            'temperature': entry.r.temperature,
            'voltage_open_circuit': entry.r.voltage_open_circuit,
            'internal_series_resistance': entry.r.internal_series_resistance,
            'internal_impedance': entry.r.internal_impedance
        })
    
    return jsonify(result), 200

