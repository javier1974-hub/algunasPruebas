from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from random import randint
import serial
import numpy as np

i = 0
k = 100
n = 5000
cont = 0
N = 0

offset = 56500
factor = 2000

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # initialize serial port
        self.ser = serial.Serial()
        self.ser.port = "COM3"  # Arduino serial port
        self.ser.baudrate = 5000000
        self.ser.timeout = None  # specify timeout when using readline()
        self.ser.open()
        if self.ser.is_open == True:
            print("\nAll right, serial port now open. Configuration:\n")
            print(self.ser, "\n")  # print serial parameters

        self.ser.flush()

        self.graphWidget = pg.PlotWidget()
        #self.graphWidget.setLabel('left', 'Value', units='V')

        plotItem = self.graphWidget.getPlotItem()

        #axBottom = plotItem.getAxis('bottom')  # get x axis
        #xTicks = [0.2, 0.04]
        #axBottom.setTickSpacing(xTicks[0], xTicks[1])  # set x ticks (major and minor)


        #axLeft = plotItem.getAxis('left')  # get y axis
        #yTicks = [20000, 4000]
        #axLeft.setTickSpacing(yTicks[0], yTicks[1])  # set y ticks (major and minor)


        plotItem.showGrid(x=True, y=True, alpha=0.8)


        self.setCentralWidget(self.graphWidget)


        self.x = np.zeros((n), dtype=np.float32)
        self.y = np.zeros((n), dtype=np.float32)
        self.R = np.zeros((n), dtype=np.float32)

        self.x[:] = np.linspace((N * k), (n + (N * k)) - 1, n)

        self.y_uart = np.zeros(k)
        self.R_uart = np.zeros(k)

        self.graphWidget.setBackground('k')


        pen = pg.mkPen(color='r', width=2)
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        pen1 = pg.mkPen(color='g', width=3)
        self.data_line1 = self.graphWidget.plot(self.x, self.R, pen=pen1)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def update_plot_data(self):
        global k, i, N, cont

        while i < k:
            inicio_dato = self.ser.read(1)
            if inicio_dato == b'\x24':
                dato_uart_byte = self.ser.read(5)
                fin_dato = self.ser.read(1)
                if fin_dato == b'\x23':
                    self.y_uart[i] = int.from_bytes(dato_uart_byte[0:4], byteorder='big', signed=True)
                    self.R_uart[i] = int.from_bytes(dato_uart_byte[4:], byteorder='big', signed=True)
                    i = i + 1
                # else:
                # fin_dato = ser.read(1)
            else:
                pass
        else:
            i = 0

        self.x[:] = np.linspace((N * k), (n + (N * k)) - 1, n)
        self.y[:-k] = self.y[k:]      # primero corro k a la izquierda
        self.R[:-k] = self.R[k:]
        self.y[-k:] = self.y_uart[:]  + offset # luego agrego los nuevos k valores a graficar
        self.R[-k:] = self.R_uart[:] * factor

        self.data_line.setData(self.x,self.y)  # Update the data.
        self.data_line1.setData(self.x,(-1)*self.R+14000)  # Update the data.

        N = N + 1


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())