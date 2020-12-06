import time
import busio
import adafruit_bme680
import logger
import serial
from digitalio import DigitalInOut, Direction, Pull
import adafruit_pm25

reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

pm25 = adafruit_pm25.PM25_UART(uart, reset_pin)

i2c = busio.I2C(3,2)
print(i2c.scan())
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

bme680.sea_level_pressure = 1012.53
temperature_offset = -1
 
while True:
    temp = int(bme680.temperature) + temperature_offset
    logger.log(pm25.read()["particles 25um"], (temp + temperature_offset) * 9/5 + 32, bme680.humidity, bme680.pressure / 33.864)
    time.sleep(60)