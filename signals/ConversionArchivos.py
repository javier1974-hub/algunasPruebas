
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import random

path_signal = 'D:/Proyectos/ECG_SINCRONIZADOR_CARDIACO/9_D&D/3_SINCRONIZADOR_CARDIACO_Disenio/Prueba_Serie/signals/train/'
path_signal_c = 'D:/Proyectos/ECG_SINCRONIZADOR_CARDIACO/9_D&D/3_SINCRONIZADOR_CARDIACO_Disenio/Prueba_Serie/signals/train_c/'

path_masks = 'D:/Proyectos/ECG_SINCRONIZADOR_CARDIACO/9_D&D/3_SINCRONIZADOR_CARDIACO_Disenio/Prueba_Serie/signals/train_masks/'
path_masks_c = 'D:/Proyectos/ECG_SINCRONIZADOR_CARDIACO/9_D&D/3_SINCRONIZADOR_CARDIACO_Disenio/Prueba_Serie/signals/train_masks_c/'

fileList = os.listdir(path_signal)
print(fileList)
for file in fileList:
    data = np.genfromtxt(path_signal + file, delimiter=",")
    data=np.transpose(data)
    #np.savetxt(path_signal_c + file, [data], delimiter=",")  # no anda
    np.savetxt(path_signal_c + file, data, delimiter=",\n")      #tampoco anda
    #np.savetxt(path_signal_c + file, data, delimiter=",", newline="\n")

# fileList = os.listdir(path_masks)
# print(fileList)
# for file in fileList:
#     data = np.genfromtxt(path_masks + file, delimiter=",")
#     data=np.transpose(data)
#     #np.savetxt(path_c + file, [data], delimiter=",")   no anda
#     #np.savetxt(path_c + file, data, newline=",")      tampoco anda
#     np.savetxt(path_masks_c + file, data, delimiter=",", newline="\n")
#
