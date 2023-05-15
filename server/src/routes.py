from flask import jsonify
from app import app
from .models import Battery, TimeSeriesData

## get all battery
@app.route("/data", methods = ["GET"])
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
@app.route("/data/<battery_id>", methods = ["GET"])
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
