import time
import board
import busio
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from machine import Pin

led = Pin(25,Pin.OUT)
led.value(1)

i2c = busio.I2C(board.GP1, board.GP0)
dhcx = ISM330DHCX(i2c)

accelGyroLog = open("/rowData/accelXYSquare0.csv", "a")

startTime = time.ticks_us()

counter = 2000
while counter>0:
    counter-=1
    acceleration = dhcx.acceleration
    # gyroscope = dhcx.gyro
    timeInterval = time.ticks_diff(time.ticks_us(),startTime)/1000000 # seconds
    startTime = time.ticks_us()
    accelGyroLog.write("{0},{1},{2}\n".format(str(timeInterval),str(acceleration[0]),str(acceleration[1])))
led.value(0)