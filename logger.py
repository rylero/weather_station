from influxdb import InfluxDBClient
from time import gmtime, strftime

temp_body = [
{
    "measurement": "weather_sensor",
    "tags": {
        "location": "office"
    },
    "time": "2020-10-10T11:00:00Z",
    "fields": {
        "temp": 70.3
    }
}
]

pressure_body = [
{
    "measurement": "weather_sensor",
    "tags": {
        "location": "office"
    },
    "time": "2020-10-10T11:00:00Z",
    "fields": {
        "pressure": 29.92
    }
}
]

humidity_body = [
{
    "measurement": "weather_sensor",
    "tags": {
        "location": "office"
    },
    "time": "2020-10-10T11:00:00Z",
    "fields": {
        "humidity": 60.32
    }
}
]

air_body = [
{
    "measurement": "weather_sensor",
    "tags": {
        "location": "office"
    },
    "time": "2020-10-10T11:00:00Z",
    "fields": {
        "airquality": 60.32,
        "pm25_standard": 50.00,
        "pm25_env": 50.00,
        "pm25_um":  50.00
    }
}
]

client = InfluxDBClient('homeassistant.local', 8086, 'home_assistant', 'home_assistant', 'weather_station')

# Only required for first time this program was run
# client.create_database('weather_station')


def log(aqi, pm25_standard, pm25_env, pm25_um, temp, humidity, pressure):
    temp_body[0]["time"] = strftime("%Y-%m-%d", gmtime())+"T"+strftime("%H:%M:%S", gmtime())+"Z"
    humidity_body[0]["time"] = strftime("%Y-%m-%d", gmtime())+"T"+strftime("%H:%M:%S", gmtime())+"Z"
    pressure_body[0]["time"] = strftime("%Y-%m-%d", gmtime())+"T"+strftime("%H:%M:%S", gmtime())+"Z"
    air_body[0]["time"] = strftime("%Y-%m-%d", gmtime())+"T"+strftime("%H:%M:%S", gmtime())+"Z"

    temp_body[0]["fields"]["temp"] = temp
    humidity_body[0]["fields"]["humidity"] = humidity
    pressure_body[0]["fields"]["pressure"] = pressure
    air_body[0]["fields"]["airquality"] = aqi
    air_body[0]["fields"]["pm25_standard"] = pm25_standard
    air_body[0]["fields"]["pm25_env"] = pm25_env
    air_body[0]["fields"]["pm25_um"] = pm25_um

    # wrap all these write calls around a try block
    try:
        client.write_points(temp_body)
        client.write_points(humidity_body)
        client.write_points(pressure_body)
        client.write_points(air_body)
    except:
        pass

