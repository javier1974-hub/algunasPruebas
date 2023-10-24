import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import wfdb
import ecg_plot
from scipy.spatial import distance

#signal = np.genfromtxt('.\sujeto104_5.csv',dtype = float, delimiter =',')

#signal, fields = wfdb.rdsamp('sample-data/s0010_re', channels=[0], sampfrom=0, sampto='end')
#signals2, fields2 = wfdb.rdsamp('s0010_re', channels=[14, 0, 5, 10], sampfrom=100, sampto=15000, pn_dir='ptbdb/patient001/')
#signal, fields2 = wfdb.rdsamp('s0014lre', channels=[0], pn_dir='ptbdb/patient001/')
# signal, fields2 = wfdb.rdsamp('sel100', channels=[1], pn_dir='qtdb/')
# signal = np.squeeze(signal)

# lee QTDB con WFDB

inicio_anotaciones=150000
fin_anotaciones = 156000
signals2, fields2 = wfdb.rdsamp('.\sel31', channels=[0,1], sampfrom=inicio_anotaciones, sampto=fin_anotaciones)
annotation = wfdb.rdann('.\sel31', 'q1c', sampfrom=inicio_anotaciones, sampto=fin_anotaciones)
#atribute = wfdb.rdann('.\sel102', 'atr', sampfrom=inicio_anotaciones, sampto=fin_anotaciones)
#
# print(signals2)
# print(fields2)
#

#ecg_plot.plot_1(signals2[0:250,0], sample_rate=250, title='Malignant Ventricular Fibrillation')
#ecg_plot.plot_1(signals2[0:250,1], sample_rate=250, title='')
#ecg_plot.show()

distancia1 = distance.euclidean(signals2[0:250,0],signals2[250:500,0])
distancia2 = distance.euclidean(signals2[0:250,0],signals2[0:250,1])

N = int(len(signals2[:,0])/250)

distancia_Ch0 = np.zeros(N)
distancia_Ch1 = np.zeros(N)
distancia_Ch01 = np.zeros(N)
distancia_Ch10 = np.zeros(N)

for i in range(N):
    distancia_Ch0[i] = distance.euclidean(signals2[(i*N):((i*N)+250),0],signals2[((i+1)*N):(((i+1)*N)+250),0])
    distancia_Ch1[i] = distance.euclidean(signals2[(i*N):((i*N)+250),1], signals2[((i+1)*N):(((i+1)*N)+250), 1])
    distancia_Ch01[i] = distance.euclidean(signals2[(i*N):((i*N)+250),0], signals2[((i+1)*N):(((i+1)*N)+250), 1])
    distancia_Ch10[i] = distance.euclidean(signals2[(i*N):((i*N)+250),1], signals2[((i+1)*N):(((i+1)*N)+250), 0])


fig = go.Figure()
t=np.linspace(1,len(distancia_Ch0), len(distancia_Ch0))

fig.add_trace(go.Scatter(x=t, y= distancia_Ch0, mode='lines',name='ch0'))
fig.add_trace(go.Scatter(x=t, y= distancia_Ch1, mode='lines',name='ch1'))
fig.add_trace(go.Scatter(x=t, y= distancia_Ch01, mode='lines',name='ch01'))
fig.add_trace(go.Scatter(x=t, y= distancia_Ch10, mode='lines',name='ch10'))
#fig.add_trace(go.Scatter(x=posQRS, y=x[posQRS], mode='markers',name='markers'))
fig.show()

print('distancia media Ch0: ' + str(np.mean(distancia_Ch0)))
print('distancia media Ch1: ' + str( np.mean(distancia_Ch1)))
print('distancia media Ch0: ' +  str(np.mean(distancia_Ch01)))
print('distancia media Ch1: ' + str( np.mean(distancia_Ch10)))