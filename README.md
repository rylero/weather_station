# weather_station
This project is my home weather station hosted on a Raspberry Pi 4
Today it includes the following sensors:
    - Temperature
    - Barometric Pressure
    - Relative Humidity
    - Air Quality
    
The weather station starts as a service on boot of the Pi. It periodically polls the sensors and then sends the readings to an InfluxDb hosted on our household NAS.
From there I use the InfluxDb data to populate a Grafana Dashboard

