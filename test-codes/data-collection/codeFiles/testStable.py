import time
import board
import busio
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from machine import Pin

led = Pin(25,Pin.OUT)

i2c = busio.I2C(board.GP1, board.GP0)
dhcx = ISM330DHCX(i2c)
accelPast = dhcx.acceleration

while True:
    time.sleep_ms(10)
    led.value(0)
    accel = dhcx.acceleration
    gyro =  dhcx.gyro
    
    if abs(gyro[0])>0.01 or abs(gyro[1])>0.01 or abs(gyro[2])>0.01 or abs(accelPast[0]-accel[0])>0.2 or abs(accelPast[1]-accel[1])>0.2 or abs(accelPast[2]-accel[2])>0.2:
        led.value(1)
        print(str(gyro)+"-"+str(accel))
    accelPast = accel