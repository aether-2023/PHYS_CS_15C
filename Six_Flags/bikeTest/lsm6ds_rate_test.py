# SPDX-FileCopyrightText: Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import board
import time
# pylint:disable=no-member,unused-import
from adafruit_lsm6ds import Rate
# from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS

# from adafruit_lsm6ds.lsm6ds33 import LSM6DS33 as LSM6DS
# from adafruit_lsm6ds.lsm6dso32 import LSM6DSO32 as LSM6DS
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX as LSM6DS

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = LSM6DS(i2c)

#while True:
sensor.accelerometer_data_rate = Rate.RATE_12_5_HZ
sensor.gyro_data_rate = Rate.RATE_12_5_HZ

timeList = []
i = 0
while i<10000:
    if i==0:
        timeList.append([time.time_ns()])
    if i==9999:
        timeList.append([time.time_ns()])
    a = sensor.acceleration
    i+=1 
        
    #print("(%.2f, %.2f, %.2f, %.2f, %.2f, %.2f" % (sensor.acceleration + sensor.gyro))
print((10**9)*10000/(timeList[-1][0]-timeList[0][0]))

timeList = []
sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
i = 0
while i<10000:
    i+=1 
    timeList.append([time.time_ns(),sensor.acceleration,sensor.gyro])
print((10**9)*10000/(timeList[-1][0]-timeList[0][0]))

timeList = []
sensor.accelerometer_data_rate = Rate.RATE_6_66K_HZ
sensor.gyro_data_rate = Rate.RATE_6_66K_HZ
i = 0
while i<10000:
    i+=1 
    timeList.append([time.time_ns(),sensor.acceleration,sensor.gyro])
print((10**9)*10000/(timeList[-1][0]-timeList[0][0]))
