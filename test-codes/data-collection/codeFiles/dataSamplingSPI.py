import time
import board
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

spi = board.SPI()
dhcx = ISM330DHCX(spi)

dataFileName = "../dataFiles/accelGyroLog"+input('Enter the filename here: ')+".csv"
accelGyroLog = open(dataFileName, "a")

startTime = time.time_ns()
#take finite amount of data

for counter in range(1000000):
    #take rest data for calibration
    if counter == 0:
       print('Ready!')
    
    accel = dhcx.acceleration
    gyro =  dhcx.gyro
    timeInterval = (time.time_ns() - startTime)/1000000000 # seconds
    startTime = time.time_ns()
    accelGyroLog.write("{0},{1},{2},{3},{4},{5},{6}\n".format(str(timeInterval), \
                                          str(accel[0]),str(accel[1]),str(accel[2]), \
                                          str(gyro[0]),str(gyro[1]),str(gyro[2])))
    
accelGyroLog.close()

print('Done!')