import psycopg2
import datetime

conn = psycopg2.connect(
    database="temperature_sensor",
    user="postgres",
    host="192.168.0.104",
    password="3logytech!"
)

message_json = {
    "battery_id": 1,
    "ble_uuid": "bdsadjgosaf",
    "humidity": 123.2141,
    "temperature": 12.455,
    "internal_series_resistance": 235.663,
    "internal_impedance": 231.42425,
    "timestamp": str(datetime.datetime.now())
}



print("db connected")
print(conn)
cursor = conn.cursor()
try:

    q = """
    INSERT INTO readings (battery_id, ble_uuid, humidity, temperature, internal_series_resistance, internal_impedance, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (
        message_json["battery_id"],
        message_json["ble_uuid"],
        message_json["humidity"],
        message_json["temperature"],
        message_json["internal_series_resistance"],
        message_json["internal_impedance"],
        message_json["timestamp"]
    )


    query = "INSERT INTO readings(battery_id, ble_uuid, humidity, temperature, internal_series_resistance, internal_impedance, timestamp) VALUES (" +\
        str(message_json["battery_id"]) + ", " + \
        message_json["ble_uuid"] + ", " + \
        str(message_json["humidity"]) + ", " + \
        str(message_json["temperature"]) + ", " + \
        str(message_json["internal_series_resistance"]) + ", " + \
        str(message_json["internal_impedance"]) + ", '" + \
        message_json["timestamp"] +"')"
    
    cursor.execute(q, values)
    conn.commit()
    print("real inserted into PSQL successfully")
except Exception as e:
    print("real Error occurred while inserting data into PostgreSQL:", str(e))
    conn.rollback()
    
finally:
    # Close the database connection
    cursor.close()
    conn.close()