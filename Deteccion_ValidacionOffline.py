import numpy as np
import pyqtgraph as pg
import pyqtgraph.examples
#pyqtgraph.examples.run()
import plotly.graph_objects as go


data = np.fromfile("output_2023-10-18_16-09-11.log",dtype='byte')

LARGO_TRAMA = 15


ecg = []
derivada = []
umbral = []
R = []

pos = 0
while pos < len(data):
    ecg.append(int.from_bytes(data[(pos + 1):(pos + 5)], byteorder='big',signed=True))
    derivada.append(int.from_bytes(data[(pos + 5):(pos + 9)], byteorder='big',signed=True))
    umbral.append(int.from_bytes(data[(pos + 9):(pos + 13)], byteorder='big',signed=True))
    R.append(int.from_bytes(data[(pos + 13):(pos + 14)], byteorder='big',signed=False))
    pos = pos + LARGO_TRAMA


#print(umbral)
ecg = np.asarray(ecg)
ecg = ecg.astype('float64')

derivada = np.asarray(derivada)
derivada = derivada.astype('float64')

umbral = np.asarray(umbral)
umbral = umbral.astype('float64')


#print(umbral)

R = np.asarray(R)
R = R.astype('float64')


posR = np.where(R==1)
#print(posR)
posR = np.squeeze(posR)

t = np.linspace(1,len(ecg),len(ecg))
offset = 0


fig = go.Figure()

# fig.add_trace(go.Scatter(x = t, y = ecg + 56429, mode='lines',name='ecg'))
# fig.add_trace(go.Scatter(x = posR, y = ecg[posR-1] + 56429, mode='markers',name='markers'))
fig.add_trace(go.Scatter(x = t, y = ecg + 56429, mode='lines',name='valor absoluto de la derivada'))
fig.add_trace(go.Scatter(x = posR, y = ecg[posR-1] + 56429, mode='markers',name='markers'))
fig.add_trace(go.Scatter(x = t, y = umbral , mode='lines',name='umbral'))
fig.add_trace(go.Scatter(x = t, y = derivada, mode='lines',name='derivada'))
fig.add_trace(go.Scatter(x = posR, y = derivada[posR-1] , mode='markers',name='markers'))

fig.show()



if __name__ == '__main__':
    pg.exec()