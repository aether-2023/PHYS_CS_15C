"""
@author: Sig Flags (Xinyuan Lin, Jichen Zhang, Bangda Zhou)
"""
import numpy as np

def calibrator(target_list, t_list):
    index = 1000 # use first 1000 measures to calibrate
    calibration_a = sum(target_list[:index])/index
    calibrated_list = target_list - calibration_a
    return calibrated_list

def get_1dtraj(accel_list, t_interval_list, threshold=0.004):
    v_list = [0]
    for index in range(len(accel_list)):
        if index>0:
            v = t_interval_list[index]*accel_list[index]+v_list[index-1]
            if abs(v)<threshold:
                v_list.append(0)
            else:
                v_list.append(v)
    v_list = np.array(v_list)
    x_list = [0]
    for index in range(len(accel_list)):
        if index>0:
            x = (t_interval_list[index]**2)*accel_list[index]/2+v_list[index]*t_interval_list[index]+x_list[index-1]
            x_list.append(x)
    x_list = np.array(x_list)
    return v_list, x_list

def get_3dabsaccel(accel_list, ):
    pass

def get_noisereduce()
