# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 16:43:03 2022

@author: javier
"""

import sys
import numpy as np
import vispy
from vispy import scene, app, visuals
from vispy.scene import visuals
# import pandas as pd
import serial

vispy.use(app='PyQt5')

# Tambien hay que installar pyQt y jupiter-rbf

# initialize serial port
ser = serial.Serial()
ser.port = "COM3"  # Arduino serial port
ser.baudrate = 5000000
ser.timeout = None  # specify timeout when using readline()
ser.open()
if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters

ptr = 0
ser.flush()

N = 0
k = 100  # acualiza cada 100 muestras
n = 3000

# vertex positions of data to draw
dato_prueba = np.zeros((n, 3), dtype=np.float32)
dato_prueba_uart_int = np.zeros((k, 3), dtype=np.float32)

dato_prueba[:, 0] = np.linspace(0, n - 1, n)

# factor de amplitud, como para que se vea
factor = -0.00000014305

# # vertex positions of data to draw
pos = np.zeros((n, 2), dtype=np.float32)
pos1 = np.zeros((n, 2), dtype=np.float32)

color = np.ones((n, 4), dtype=np.float32)
color[:, 0] = np.linspace(0, 1, n)
color[:, 1] = color[::-1, 0]
color[:, 2] = color[::-1, 0]


canvas = scene.SceneCanvas(keys='interactive', show=True)
grid = canvas.central_widget.add_grid(spacing=0)


viewbox = grid.add_view(row=0, col=1, camera='panzoom')
viewbox.camera.set_range()
# add some axes
x_axis = scene.AxisWidget(orientation='bottom')
x_axis.stretch = (1, 0.1)
grid.add_widget(x_axis, row=1, col=1)
x_axis.link_view(viewbox)

y_axis = scene.AxisWidget(orientation='left')
y_axis.stretch = (0.1, 1)
grid.add_widget(y_axis, row=0, col=0)
y_axis.link_view(viewbox)

i = 0

def update(ev):
    global pos, pos1, color, line, N, k, i

    while i < k:
        inicio_dato = ser.read(1)
        if inicio_dato == b'\x24':
            dato_uart_byte = ser.read(5)
            fin_dato = ser.read(1)
            if fin_dato == b'\x23':
                dato_prueba_uart_int[i, 1] = int.from_bytes(dato_uart_byte[0:4], byteorder='big', signed=True)
                dato_prueba_uart_int[i, 2] = int.from_bytes(dato_uart_byte[4:], byteorder='big', signed=True)
                i = i + 1
            #else:
               # fin_dato = ser.read(1)
        else:
            pass
    else:
        i = 0

    ser.flush()
    dato_prueba[:, 0] = np.linspace((N * k), (n + (N * k)) - 1, n)

    dato_prueba[-k:, 1] = np.nan
    dato_prueba[-k:, 1] = (dato_prueba_uart_int[:, 1] + 56545)  # le sumo este valor medio gigantesco y lo escalo
    dato_prueba[-k:, 2] = (dato_prueba_uart_int[:, 2] * 15000)


    pos[:, 0] = dato_prueba[:, 0]
    pos[:, 1] = dato_prueba[:, 1]
    pos1[:, 0] = dato_prueba[:, 0]
    pos1[:, 1] = dato_prueba[:, 2]



    line = visuals.Line(pos=pos, parent=viewbox.scene)
    line1 = visuals.Line(pos=pos1, parent=viewbox.scene)
    #p1 = visuals.Markers(pos=pos1, parent=viewbox.scene)



    # aca tengo que correr k a la izq. los elementos de dato_prueba[:,1]
    dato_prueba[:-k, 1] = dato_prueba[k:, 1]
    dato_prueba[:-k, 2] = dato_prueba[k:, 2]


    color = np.roll(color, 1, axis=0)
    line.set_data(pos=pos, color='r')
    #line1.set_data(pos=pos1, color='w')
    #p1.set_data(pos = pos1, face_color='w', symbol="o", size=30, edge_width=0.5, edge_color="blue" )

    #print(pos1[:,1])

    viewbox.camera.set_range(x=((N * k), (n + (N * k))), y=(dato_prueba[:, 1].min(), dato_prueba[:, 1].max()))
    #viewbox.camera.set_range(x=((N * k), (n + (N * k))), y=(-2500, dato_prueba[:, 1].max()))
    N = N + 1


timer = app.Timer(0.01, connect=update, start=True)

if __name__ == '__main__' and sys.flags.interactive == 0:
    app.run()