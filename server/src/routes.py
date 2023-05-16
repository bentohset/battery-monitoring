from flask import jsonify, current_app, Blueprint
from .models import Battery, TimeSeriesData

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

# TODO: get data over time
@routes.route("/data/<battery_id>", methods = ["GET"])
def get_by_id(battery_id):
    data = TimeSeriesData.query.filter_by(battery_id=battery_id).order_by(TimeSeriesData.timestamp.asc()).all()

    # get over time
    result = []
    for entry in data:
        result.append({
            'timestamp': entry.timestamp,
            'impedance': entry.impedance,
            'humidity': entry.humidity,
            'temperature': entry.temperature
        })

    return jsonify(result), 200

## update battery name?
