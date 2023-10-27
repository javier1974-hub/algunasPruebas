import numpy as np
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
QLineEdit, QCheckBox, QTextEdit, QGridLayout,QPushButton,QFileDialog, QTableWidget, QTableWidgetItem,QProgressBar)
from PyQt6 import QtCore
from pyqtgraph import PlotWidget, plot
from PyQt6.QtCore import pyqtSignal, QThread
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from time import sleep
import os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import numpy as np
import os
import random
import itertools
import serial


i = 0
k = 100
n = 5000
cont = 0
N = 0

offset = 56500
factor = 2000















class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initializeUI()

    def initializeUI(self):
        """Set up the application's GUI."""
        self.setMinimumSize(1000, 800)
        self.setWindowTitle('Segmentacion de PCG')
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):

        self.win = pg.GraphicsLayoutWidget(show=True)
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)

        self.p1 =self.win.addPlot(row=0, col=0)
        # customize the averaged curve that can be activated from the context menu:
        self.p1.avgPen = pg.mkPen('#FFFFFF')
        self.p1.avgShadowPen = pg.mkPen('#8080DD', width=10)

        self.x = np.zeros((n), dtype=np.float32)
        self.y = np.zeros((n), dtype=np.float32)
        self.R = np.zeros((n), dtype=np.float32)

        self.x[:] = np.linspace((N * k), (n + (N * k)) - 1, n)

        self.y_uart = np.zeros(k)
        self.R_uart = np.zeros(k)

        #self.p1.setBackground('k')
        self.p1.showGrid(x=True, y=True, alpha=0.8)

        pen = pg.mkPen(color='r', width=2)
        self.data_line = self.p1.plot(self.x, self.y, pen=pen)
        pen1 = pg.mkPen(color='g', width=3)
        self.data_line1 = self.p1.plot(self.x, self.R, pen=pen1)

        self.bpm= QLabel("",self)


        self.button_Connect = QPushButton("Connect",self)
        self.button_Connect.clicked.connect(self.buttonConnectClicked)
        self.button_Disconnect = QPushButton("Disconnect",self)
        self.button_Disconnect.clicked.connect(self.buttonDisconnectClicked)


        #self.table = QTableWidget(4,2)

        # self.items_grid = QGridLayout()
        # self.items_grid.addWidget(self.win , 0, 1, 5,1)
        # self.items_grid.addWidget(self.button_Connect, 0, 0, 1,1)
        # self.items_grid.addWidget(self.button_Disconnect, 2, 0, 1, 1)
        # self.items_grid.addWidget(self.bpm, 3, 0, 1, 1)

        self.items_grid = QGridLayout()
        self.items_grid.addWidget(self.win , 0, 0, 9, 2)
        self.items_grid.addWidget(self.button_Connect, 10, 0, 1, 1)
        self.items_grid.addWidget(self.button_Disconnect, 10, 1, 1, 1)
        self.items_grid.addWidget(self.bpm, 3, 0, 1, 1)


        self.setLayout(self.items_grid)



    def buttonConnectClicked(self, evt):
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

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

    def buttonDisconnectClicked(self):


        # self.file_name, ok = QFileDialog.getOpenFileName(self,"Open File", "","csv (*.csv) ")
        #
        # self.worker = Worker(self.file_name, self.pcg)
        #
        # self.worker.progress.connect(self.updateProgressBar)
        #
        # self.worker.start()
        #
        # self.worker.finished.connect(self.graficar)

        pass


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


    def graficar(self,data):
        self.pcg = data
        self.time = np.arange(0, len(self.pcg), 1, dtype=np.float32)

        self.p1.plot(self.pcg, pen="r", symbol='o', symbolSize=5, symbolBrush="r")
        self.p1.showGrid(x=True, y=True, alpha=0.3)
        # self.p1.plot(data2, pen="g")

        p2d = self.p2.plot(self.pcg, pen="w")
        # bound the LinearRegionItem to the plotted data
        self.region.setClipItem(p2d)

        self.region.sigRegionChanged.connect(self.update)
        self.p1.sigRangeChanged.connect(self.updateRegion)

        self.region.setRegion([0, 1024])

        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        self.vb = self.p1.vb
        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)
        self.p1.scene().sigMouseClicked.connect(self.mouseClicked)

        self.button_Segment.setEnabled(True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())