import time
import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
import pickle

i2c = board.I2C()
dhcx = ISM330DHCX(i2c)

dataFileName = "./dataFiles/sf"+input('Enter the filename here: ')

timeList = []
acceList = []
gyroList = []

#take finite amount of data
counter = int(input('Duration (s): '))*500

for i in range(counter):
    timeList.append(time.time())
    acceList.append(dhcx.acceleration)
    gyroList.append(dhcx.gyro)

print('Dumping data!')

accelGyroLog = open(dataFileName, 'wb')   
pickle.dump([timeList,acceList,gyroList],accelGyroLog) 
accelGyroLog.close()

