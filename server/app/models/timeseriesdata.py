from app.extensions import db
from datetime import datetime

# | id | battery_id(int) | ble_uuid(int) | humidity(numeric/decimal) | temperature(numeric) 
# | voltage_open_circuit(numeric) | internal_series_resistance(numeric) | internal_impedance(numeric) | 
class TimeSeriesData(db.Model):
    """Read only, data retrieved from hardware
    """

    __tablename__ = "readings"

    id = db.Column(db.Integer, primary_key=True)
    battery_id = db.Column(db.Integer, db.ForeignKey('batteries.id'))
    ble_uuid = db.Column(db.String(255), nullable=False)
    humidity = db.Column(db.Float)
    temperature = db.Column(db.Float)
    internal_series_resistance = db.Column(db.Float)
    internal_impedance = db.Column(db.Float)
    timestamp = db.Column(db.TIMESTAMP) # recorded every few hours
    # 2023-06-01 09:12:40.466997

    battery = db.relationship('Battery', backref=db.backref('readings', lazy=True))

    def __init__(self, battery_id:int, ble_uuid:str, humidity:float, temp:float, isr:float, ii:float, timestamp:str ):
        """For testing purposes"""
        
        self.battery_id = battery_id
        self.ble_uuid = ble_uuid
        self.humidity = humidity
        self.temperature = temp
        self.internal_series_resistance = isr
        self.internal_impedance = ii
        
        # datetime_str = '19/09/22 13:55:26'
        self.timestamp = datetime.strptime(timestamp, '%d/%m/%y %H:%M:%S')