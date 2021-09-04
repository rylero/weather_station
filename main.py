import time
import busio
import math
import adafruit_bme680
import logger
import serial
import adafruit_pm25


#
# https://www.airnow.gov/sites/default/files/custom-js/conc-aqi.js
# the Adafruit Air Quality sensor returns various values, but none match Purple Air. This will translate
# the "pm25 standard" value from the sensor into the "US EPA PM2.5 AQI" value.
#
def linear(aqihigh, aqilow, conchigh, conclow, concentration):

    conc = float(concentration)
    a = ((conc - conclow) / (conchigh - conclow)) * (aqihigh - aqilow) + aqilow
    lin = round(a)
    return lin


def aqi_pm25(concentration):

    conc = float(concentration)
    c = (math.floor(10 * conc)) / 10

    if 0 <= c < 12.1:
        aqival = linear(50, 0, 12, 0, c)
    elif 12.1 <= c < 35.5:
        aqival = linear(100, 51, 35.4, 12.1, c)
    elif 35.5 <= c < 55.5:
        aqival = linear(150, 101, 55.4, 35.5, c)
    elif 55.5 <= c < 150.5:
        aqival = linear(200, 151, 150.4, 55.5, c)
    elif 150.5 <= c < 250.5:
        aqival = linear(300, 201, 250.4, 150.5, c)
    elif 250.5 <= c < 350.5:
        aqival = linear(400, 301, 350.4, 250.5, c)
    elif 350.5 <= c < 500.5:
        aqival = linear(500, 401, 500.4, 350.5, c)
    else:
        aqival = 0
    return int(aqival)


# Setup serial interface to talk with air quality sensor.
reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)

# Setup I2C bus to talk with humidity, temp, pressure sensor.
i2c = busio.I2C(3, 2)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# Setup some offsets to provide more accurate sensor readings
temperature_offset = -1
pressure_offset = 0.38 
 
while True:
    temp = int(bme680.temperature) + temperature_offset
    # Example on how to setup air quality reading
    # https://github.com/adafruit/Adafruit_CircuitPython_PM25/blob/main/examples/pm25_simpletest.py
    aqdata = pm25.read()
    pm25_standard = aqdata["pm25 standard"]
    pm25_env = aqdata["pm25 env"]
    pm25_um = aqdata["particles 25um"]
    aqi = aqi_pm25(pm25_standard)
    logger.log(aqi,
               pm25_standard,
               pm25_env,
               pm25_um,
               (temp + temperature_offset) * 9/5 + 32,
               bme680.humidity,
               (bme680.pressure / 33.864) + pressure_offset)
    time.sleep(60)
