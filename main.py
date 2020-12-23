import time
import busio
import math
import adafruit_bme680
import logger
import serial
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25

#
# https://www.airnow.gov/sites/default/files/custom-js/conc-aqi.js
# the Adafruit Air Quality sensor returns various values, but none match Purple Air. This will translate
# the "pm25 standard" value from the sensor into the "US EPA PM2.5 AQI" value.
#
def Linear(AQIhigh, AQIlow, Conchigh, Conclow, Concentration):

    Conc=float(Concentration)
    a=((Conc-Conclow)/(Conchigh-Conclow))*(AQIhigh-AQIlow)+AQIlow
    linear=round(a)
    return linear


def AQIPM25(Concentration):

    Conc=float(Concentration)
    c=(math.floor(10*Conc))/10

    if 0 <= c <= 12.1:
        AQI=Linear(50,0,12,0,c)
    elif (c>=12.1 and c<35.5):
        AQI=Linear(100,51,35.4,12.1,c)
    elif (c>=35.5 and c<55.5):
        AQI=Linear(150,101,55.4,35.5,c)
    elif (c>=55.5 and c<150.5):
        AQI=Linear(200,151,150.4,55.5,c)
    elif (c>=150.5 and c<250.5):
        AQI=Linear(300,201,250.4,150.5,c)
    elif (c>=250.5 and c<350.5):
        AQI=Linear(400,301,350.4,250.5,c)
    elif (c>=350.5 and c<500.5):
        AQI=Linear(500,401,500.4,350.5,c)
    else:
        AQI=0
    return int(AQI)

reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)

i2c = busio.I2C(3,2)
print(i2c.scan())
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

bme680.sea_level_pressure = 1030.5
temperature_offset = -1
pressure_offset = 0.38 
 
while True:
    temp = int(bme680.temperature) + temperature_offset
    pm25env = pm25.read()["particles 25um"]
    aqi = AQIPM25(pm25env)
    logger.log(aqi, (temp + temperature_offset) * 9/5 + 32, bme680.humidity, (bme680.pressure / 33.864) + pressure_offset)
    time.sleep(60)
