from scipy.io import loadmat

import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import wfdb

#signal = np.genfromtxt('.\sujeto104_5.csv',dtype = float, delimiter =',')

#signal, fields = wfdb.rdsamp('sample-data/s0010_re', channels=[0], sampfrom=0, sampto='end')
#signals2, fields2 = wfdb.rdsamp('s0010_re', channels=[14, 0, 5, 10], sampfrom=100, sampto=15000, pn_dir='ptbdb/patient001/')
#signal, fields2 = wfdb.rdsamp('s0014lre', channels=[0], pn_dir='ptbdb/patient001/')
signal, fields2 = wfdb.rdsamp('sel100', channels=[1], pn_dir='qtdb/')
signal = np.squeeze(signal)

# lee QTDB con WFDB

# inicio_anotaciones=150000
# fin_anotaciones = 156000
# signals2, fields2 = wfdb.rdsamp('.\sel100', channels=[0,1], sampfrom=inicio_anotaciones, sampto=fin_anotaciones)
# annotation = wfdb.rdann('.\sel100', 'q1c', sampfrom=inicio_anotaciones, sampto=fin_anotaciones)
#
# print(signals2)
# print(fields2)
#
# fig = go.Figure()
# t=np.linspace(1,len(signals2), len(signals2))
# fig.add_trace(go.Scatter(x=t, y= signals2[:,0], mode='lines',name='lines'))
# fig.add_trace(go.Scatter(x=annotation.sample-inicio_anotaciones, y=signals2[:,0][annotation.sample-inicio_anotaciones], mode='text+markers', text = annotation.symbol))
# fig.show()


h0 = np.array([0.125, 0.375, 0.375, 0.125])
g0 = np.array([2, -2])

if (fields2['fs'] == 1000):
  h = sp.upfirdn([1], h0, 4)
  g = sp.upfirdn([1], g0, 4)
  ventana = np.ones(150) / 150
if (fields2['fs'] == 250):
  h = h0
  g = g0
  ventana = np.ones(37) / 37

print(fields2['fs'])

d1=sp.convolve(signal,g, mode = 'same');
a1=sp.convolve(signal,h, mode = 'same');

h1=sp.upfirdn([1],h,2);
g1=sp.upfirdn([1],g,2);

d2=sp.convolve(a1,g1, mode = 'same');
a2=sp.convolve(a1,h1, mode = 'same');

h2=sp.upfirdn([1],h1,2);
g2=sp.upfirdn([1],g1,2);

d3=sp.convolve(a2,g2, mode = 'same');
a3=sp.convolve(a2,h2, mode = 'same');

h3=sp.upfirdn([1],h2,2);
g3=sp.upfirdn([1],g2,2);

d4=sp.convolve(a3,g3, mode = 'same');
a4=sp.convolve(a3,h3, mode = 'same');

h4=sp.upfirdn([1],h3,2);
g4=sp.upfirdn([1],g3,2);

d5=sp.convolve(a4,g4, mode = 'same');
a5=sp.convolve(a4,h4, mode = 'same');


fig = px.line(signal)
fig.show()



fig = go.Figure()
t=np.linspace(1,len(d3), len(d3))

fig.add_trace(go.Scatter(x=t, y= signal, mode='lines',name='lines'))
fig.add_trace(go.Scatter(x=t, y= np.abs(d3), mode='lines',name='lines'))
fig.add_trace(go.Scatter(x=t, y= np.abs(d2), mode='lines',name='lines'))
fig.show()




x = sp.convolve(np.abs(d2),ventana,mode='same')


fig = go.Figure()
t=np.linspace(1,len(d2), len(d2))
fig.add_trace(go.Scatter(x=t, y= x, mode='lines',name='lines'))
fig.add_trace(go.Scatter(x=t, y= np.abs(d2), mode='lines',name='lines'))
fig.show()

def rms(x):
  return np.sqrt(x.dot(x)/x.size)

thr = 2*rms(x)
print(thr)


posQRS, _ = sp.find_peaks(np.abs(x), height=thr, width = len(ventana), distance= 2*len(ventana))


fig = go.Figure()
t=np.linspace(1,len(d2), len(d2))

fig.add_trace(go.Scatter(x=t, y= x, mode='lines',name='lines'))
fig.add_trace(go.Scatter(x=posQRS, y=x[posQRS], mode='markers',name='markers'))
fig.show()

candidatosR = np.zeros((len(posQRS),2*len(ventana)))

for i in range(len(posQRS)):
  candidatosR[i] = d3[(posQRS[i]-len(ventana)):(posQRS[i]+len(ventana))]


# fig = go.Figure()
# t=np.linspace(1,len(candidatosR[1,:]), len(candidatosR[1,:]))
# for i in range(len(posQRS)-1):
#   fig.add_trace(go.Scatter(x=t, y= candidatosR[i,:], mode='lines',name='lines'))
# fig.show()



fig = go.Figure()
t=np.linspace(1,2*len(ventana), 2*len(ventana))
fig.add_trace(go.Scatter(x=t, y= np.abs(candidatosR[0,:]), mode='lines',name='d3'))
fig.show()

def Normalize(data):
  min_val = np.min(data)
  max_val = np.max(data)
  return (data - min_val) / (max_val - min_val)

nroQRS = 0
th1 = 0.2
th2 = 0.8
peaksR, _ = sp.find_peaks(np.abs(candidatosR[nroQRS,:]), height=th2)
print(peaksR)


fig = go.Figure()
t=np.linspace(1,len(candidatosR[nroQRS,:]), len(candidatosR[nroQRS,:]))
fig.add_trace(go.Scatter(x=t, y= candidatosR[nroQRS,:], mode='lines',name='d3'))
fig.add_trace(go.Scatter(x=t, y= Normalize(np.abs(candidatosR[nroQRS,:])), mode='lines',name='abs(d3) normalzada'))
fig.add_hline(y=th1, line_width=3, line_dash="dash", line_color="red")
fig.add_hline(y=th2, line_width=3, line_dash="dash", line_color="black")
fig.add_trace(go.Scatter(x=peaksR, y=Normalize(np.abs(candidatosR[nroQRS,:]))[peaksR], mode='markers',name='markers'))
fig.show()


fig = go.Figure()
t=np.linspace(1,len(candidatosR[nroQRS,:]), len(candidatosR[nroQRS,:]))
fig.add_trace(go.Scatter(x=t, y= signal[(posQRS[nroQRS]-len(ventana)):(posQRS[nroQRS]+len(ventana))], mode='lines',name='signal'))
fig.show()


peaksAbsD3Th1, _ = sp.find_peaks(Normalize(np.abs(candidatosR[nroQRS,:])), height=th1)
peaksAbsD3Th2, _ = sp.find_peaks(Normalize(np.abs(candidatosR[nroQRS,:])), height=th2)
print([peaksAbsD3Th1,peaksAbsD3Th2])

def evaluarMaximos(vector,a,b):
  # a es el que supera el umbral mas bajo
  # b es el que supera el umbral mas alto

  if (len(a) == 2 and len(b) == 2):
    if((np.sign(vector[b[0]]) > 0)   and ( np.sign(vector[b[1]]) < 0)):
      print('QRS positivo')

    if((np.sign(vector[b[0]])  < 0 ) and  (np.sign(vector[a[1]]) > 0)):
      print('QRS negativo')

  if (len(a) == 2 and len(b) == 1):
    if (np.array_equal(a[0],b[0])): # b igual al primer elemento de a
      if((np.sign(vector[a[0]]) < 0)   and  (np.sign(vector[a[1]]) > 0)):
        print('QRS bifasico : Compejo rS')
        # falta el caso con signos opuestos
      if((np.sign(vector[a[0]]) > 0)   and  (np.sign(vector[a[1]]) < 0)):
        print('QRS bifasico : Compejo qR')


    if (np.array_equal(a[1],b[0])): # b igual al segundo elemento de a
      if((np.sign(vector[a[0]]) > 0  ) and (np.sign(vector[a[1]]) < 0)):
        print('QRS bifasico : Compejo Rs')
        # falta el caso con signos opuestos if((np.sign(vector[a[0]]) < 0)   and  (np.sign(vector[a[1]]) > 0)):
      if((np.sign(vector[a[0]]) < 0)   and  (np.sign(vector[a[1]]) > 0)):
        print('QRS bifasico : Compejo Qr')

  if (len(a) == 3 and len(b) == 1):
    if(np.array_equal(a[1], b[0])): #el unico elemento de b debe ser igual al elemento del medio en a
      if((np.sign(vector[a[0]]) > 0)   and  (np.sign(vector[a[1]]) < 0) and  (np.sign(vector[a[2]]) > 0)):
        print('QRS bifasico : Compejo RS')
      if((np.sign(vector[a[0]]) < 0 )  and (np.sign(vector[a[1]]) > 0) and  (np.sign(vector[a[2]]) < 0)):
        print('QRS bifasico : Compejo QR')


  if (len(a) == 3 and len(b) == 2):
    print('longitud de a = 3 y longitud de b = 2')
    if(np.array_equal(a[:2],b[:2])): #los unicos dos elementos de b son iguales a los primeros dos elemntos de a
      if((np.sign(vector[a[0]]) > 0)   and  (np.sign(vector[a[1]]) < 0) and  (np.sign(vector[a[2]]) > 0)):
        print('QRS bifasico : Compejo Rs')
      if((np.sign(vector[a[0]]) < 0)   and  (np.sign(vector[a[1]]) > 0) and  (np.sign(vector[a[2]]) < 0)):
        print('QRS bifasico : Compejo Qr')

    if(np.array_equal(a[1:3],b[:2])): #los unicos dos elementos de b son iguales a los segundos dos elemntos de a
      if((np.sign(vector[a[0]]) < 0 )  and  (np.sign(vector[a[1]]) > 0) and  (np.sign(vector[a[2]]) < 0)):
        print('QRS bifasico : Compejo qR')
      if((np.sign(vector[a[0]]) < 0)   and  (np.sign(vector[a[1]]) > 0) and  (np.sign(vector[a[2]]) < 0)):
        print('QRS bifasico : Compejo rS')


fig = go.Figure()
t = np.linspace(1, len(candidatosR[nroQRS, :]), len(candidatosR[nroQRS, :]))

fig.add_trace(go.Scatter(x=t, y=candidatosR[nroQRS, :], mode='lines', name='d3'))
fig.add_trace(go.Scatter(x=t, y=Normalize(np.abs(candidatosR[nroQRS, :])), mode='lines', name='abs(d3) normalzada'))

fig.add_hline(y=th1, line_width=3, line_dash="dash", line_color="red")
fig.add_hline(y=th2, line_width=3, line_dash="dash", line_color="black")
fig.add_trace(go.Scatter(x=peaksR, y=Normalize(np.abs(candidatosR[nroQRS, :]))[peaksR], mode='markers', name='markers'))

fig.show()


nroQRS = 0
th1 = 0.2
th2 = 0.8
peaksAbsD3Th1, _ = sp.find_peaks(Normalize(np.abs(candidatosR[nroQRS,:])), height=th1)
peaksAbsD3Th2, _ = sp.find_peaks(Normalize(np.abs(candidatosR[nroQRS,:])), height=th2)
print([peaksAbsD3Th1,peaksAbsD3Th2])


evaluarMaximos(candidatosR[nroQRS,:],peaksAbsD3Th1,peaksAbsD3Th2)









