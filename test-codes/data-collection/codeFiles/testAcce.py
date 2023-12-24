import time
import board
import busio
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

i2c = busio.I2C(board.GP1, board.GP0)
dhcx = ISM330DHCX(i2c)
timeCounter = 0


startTime = time.ticks_us()
while True:
    #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (dhcx.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (dhcx.gyro))
    time.sleep_ms(10)
    '''
    acceleration = dhcx.acceleration
    gyroscope = dhcx.gyro
    timeInterval = time.ticks_diff(time.ticks_us(),startTime)/1000000
    startTime = time.ticks_us()
    #print("{0},{1}\n".format(str(currentTime),str(gyroscope)))
    print("{0},{1}, {2}\n".format(str(timeInterval),str(acceleration), str(gyroscope)))
    #print(acceleration[0]**2+acceleration[1]**2+acceleration[2]**2)
    '''