"""
@author: Six Flags (Xinyuan Lin, Jichen Zhang, Bangda Zhou)
"""
import numpy as np
import imufusion
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import pickle

def get_data(fileName):
    my_Data = open(fileName, 'rb')
    timeLog,acceLog,gyroLog= pickle.load(my_Data)
    my_Data.close()
    t_interval_list = [0]
    accel_3d_list = [[acceLog[0][0],acceLog[0][1],acceLog[0][2]]]
    omega_3d_list = [[gyroLog[0][0],gyroLog[0][1],gyroLog[0][2]]]
    for i in range(len(timeLog)-1):
        t_interval_list.append(timeLog[i+1]-timeLog[i])
        accel_3d_list.append([acceLog[i+1][0],acceLog[i+1][1],acceLog[i+1][2]])
        omega_3d_list.append([gyroLog[i+1][0],gyroLog[i+1][1],gyroLog[i+1][2]])
    return np.array(t_interval_list), np.array(accel_3d_list), np.array(omega_3d_list)

def get_timelist(time_interval_list):
    tot_num = len(time_interval_list)
    t_list = [time_interval_list[0]]
    for index in range(1,tot_num,1):
        t_list.append(t_list[index-1]+time_interval_list[index])
    return np.array(t_list)

def calibrator(target_list, t_list):
    index = 1500 # use first 1000 measures to calibrate
    calib_g = sum(target_list[:index])/index
    calibrated_list = target_list - calib_g
    return calibrated_list

def get_1dtraj(accel_list, t_interval_list, threshold=0.004):
    velo_list = [0]
    for index in range(1,len(accel_list),1):
        v = t_interval_list[index]*accel_list[index]+velo_list[index-1]
        if abs(v)<threshold:
            velo_list.append(0)
        else:
            velo_list.append(v)
    velo_list = np.array(velo_list)
    posi_list = [0]
    for index in range(1,len(accel_list),1):
        x = (t_interval_list[index]**2)*accel_list[index]/2+velo_list[index]*t_interval_list[index]+posi_list[index-1]
        posi_list.append(x)
    posi_list = np.array(posi_list)
    return velo_list, posi_list

def get_3dAbsAccel(accel_3d_list, omega_3d_list, t_interval_list):
    sample_rate = 250
    offset = imufusion.Offset(sample_rate)
    ahrs = imufusion.Ahrs()
    ahrs.settings = imufusion.Settings(0.5,10,0,5*sample_rate)
    omega_degree_3d_list = np.degrees(omega_3d_list)
    ahrs = imufusion.Ahrs()
    euler = np.empty((len(t_interval_list), 3))
    for index in range(len(t_interval_list)):
        omega_degree_3d_list[index] = offset.update(omega_degree_3d_list[index])
        ahrs.update_no_magnetometer(omega_degree_3d_list[index], accel_3d_list[index], t_interval_list[index]) 
        
        eulerTemp = ahrs.quaternion.to_euler()
        euler[index] = eulerTemp
        if np.isnan(eulerTemp[0]):
            euler[index][0] = euler[index-1][0]
        if np.isnan(eulerTemp[1]):
            euler[index][1] = euler[index-1][1]
        if np.isnan(eulerTemp[2]):
            euler[index][2] = euler[index-1][2]
        
    r = R.from_euler('xyz', euler, degrees=True)
    accel_3d_abs_list = r.apply(accel_3d_list)
    return euler, accel_3d_abs_list

def calibrator3d(accel_3d_list):
    accel_3d_calib_list = np.empty(accel_3d_list.shape)
    calib_g_list = []
    for indAxis in [0,1,2]:
        calib_g = sum(accel_3d_list[500:1500,indAxis])/1000
        accel_3d_calib_list[:,indAxis] = accel_3d_list[:,indAxis] - calib_g
        calib_g_list.append(calib_g)
    return accel_3d_calib_list, calib_g_list

def get_3dtraj(accel_3d_list, t_interval_list):
    velo_list = np.empty(accel_3d_list.shape)
    posi_list = np.empty(accel_3d_list.shape)
    velo_list[0] = [0,0,0]
    posi_list[0] = [0,0,0]
    for indAxis in [0,1,2]:
        for i in range(1,len(t_interval_list),1):
            newVelo = velo_list[i-1,indAxis] + accel_3d_list[i,indAxis] * t_interval_list[i]
            velo_list[i,indAxis]=newVelo
            posi_list[i,indAxis]=(posi_list[i-1,indAxis] + velo_list[i,indAxis] * t_interval_list[i])
    return velo_list, posi_list

def plot_3dAbsRotation(omega_3d_list, accel_3d_list, euler, accel_3d_abs_list, t_list):
    
    omega_degree_3d_list = np.degrees(omega_3d_list)
                              
    _, axes = plt.subplots(nrows=4, sharex=True, figsize=(15,15))
    
    axes[0].plot(t_list, omega_degree_3d_list[:, 0], "tab:red", label="X")
    axes[0].plot(t_list, omega_degree_3d_list[:, 1], "tab:green", label="Y")
    axes[0].plot(t_list, omega_degree_3d_list[:, 2], "tab:blue", label="Z")
    axes[0].set_title("Gyroscope")
    axes[0].set_ylabel("Degrees/s")
    axes[0].grid()
    axes[0].legend()
    
    axes[1].plot(t_list, accel_3d_list[:, 0], "tab:red", label="X")
    axes[1].plot(t_list, accel_3d_list[:, 1], "tab:green", label="Y")
    axes[1].plot(t_list, accel_3d_list[:, 2], "tab:blue", label="Z")
    axes[1].set_title("Accelerometer Data")
    axes[1].set_ylabel("$m/s^2$")
    axes[1].grid()
    axes[1].legend()
    
    axes[2].plot(t_list, euler[:, 0], "tab:red", label="Roll")
    axes[2].plot(t_list, euler[:, 1], "tab:green", label="Pitch")
    axes[2].plot(t_list, euler[:, 2], "tab:blue", label="Yaw")
    axes[2].set_title("Euler angles")
    axes[2].set_xlabel("Seconds")
    axes[2].set_ylabel("Degrees")
    axes[2].grid()
    axes[2].legend()
    
    axes[3].plot(t_list, accel_3d_abs_list[:, 0], "tab:red", label="X")
    axes[3].plot(t_list, accel_3d_abs_list[:, 1], "tab:green", label="Y")
    axes[3].plot(t_list, accel_3d_abs_list[:, 2], "tab:blue", label="Z")
    axes[3].set_title("Absolute Accel")
    axes[3].set_xlabel("Seconds")
    axes[3].set_ylabel("$m/s^2$")
    axes[3].grid()
    axes[3].legend()

def plot_3dAccelVeloPosi(accel_list, velo_list, posi_list, t_list):
    _, axesR = plt.subplots(nrows=3, sharex=True, figsize=(15,15))

    axesR[0].plot(t_list, accel_list[:, 0], "tab:red", label="X")
    axesR[0].plot(t_list, accel_list[:, 1], "tab:green", label="Y")
    axesR[0].plot(t_list, accel_list[:, 2], "tab:blue", label="Z")
    axesR[0].set_title("accelCalib")
    axesR[0].set_ylabel("$m/s^2$")
    axesR[0].grid()
    axesR[0].legend()
    
    axesR[1].plot(t_list, velo_list[:, 0], "tab:red", label="X")
    axesR[1].plot(t_list, velo_list[:, 1], "tab:green", label="Y")
    axesR[1].plot(t_list, velo_list[:, 2], "tab:blue", label="Z")
    axesR[1].set_title("velo_list")
    axesR[1].set_ylabel("$m/s$")
    axesR[1].grid()
    axesR[1].legend()
    
    axesR[2].plot(t_list, posi_list[:, 0], "tab:red", label="X")
    axesR[2].plot(t_list, posi_list[:, 1], "tab:green", label="Y")
    axesR[2].plot(t_list, posi_list[:, 2], "tab:blue", label="Z")
    axesR[2].set_title("posi_list")
    axesR[2].set_ylabel("$m$")
    axesR[2].grid()
    axesR[2].legend()



