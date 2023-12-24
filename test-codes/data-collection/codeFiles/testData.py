import time
import board
import busio
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

i2c = busio.I2C(board.GP1, board.GP0)
dhcx = ISM330DHCX(i2c)

accelGyroLog = open("/rowData/accelGyroData.csv", "a")

startTime = time.ticks_us()
while True:
    acceleration = dhcx.acceleration
    # gyroscope = dhcx.gyro
    timeInterval = time.ticks_diff(time.ticks_us(),startTime)/1000000 # seconds
    startTime = time.ticks_us()
    accelGyroLog.write("{0},{1}\n".format(str(timeInterval),str(acceleration[0])))
