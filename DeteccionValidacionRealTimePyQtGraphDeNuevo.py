from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
QLineEdit, QCheckBox, QTextEdit, QGridLayout,QPushButton,QFileDialog, QTableWidget, QTableWidgetItem,QProgressBar)
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal, QThread
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import numpy as np
import serial


i = 0
k = 100
n = 5000
cont_bpm = 0
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
        self.setWindowTitle('Sincronizador Validacion Deteccion')
        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):

        self.win = pg.GraphicsLayoutWidget(show=True)
        # self.label = pg.LabelItem(justify='right')
        # self.win.addItem(self.label)

        self.p1 =self.win.addPlot(row=0, col=0)
        # customize the averaged curve that can be activated from the context menu:
        self.p1.avgPen = pg.mkPen('#FFFFFF')
        self.p1.avgShadowPen = pg.mkPen('#8080DD', width=10)

        # font = QtGui.QFont()
        # font.setPixelSize(120)
        # self.text = pg.TextItem('', color='g')
        # self.text.setFont(font)
        # self.text.setText(str(0))
        # self.win.addItem(self.text)
        # self.text.setPos(500, 800)

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

        self.bpm = QLabel("",self)
        self.bpm.setStyleSheet("color: rgb(0,128,0)")
        self.bpm.setFont(QtGui.QFont('Arial', 40))
        #self.bpm.setAlignment(QtCore.Qt.AlignCenter)


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
        self.items_grid.addWidget(self.win , 1, 0, 9, 2)
        self.items_grid.addWidget(self.button_Connect, 10, 0, 1, 1)
        self.items_grid.addWidget(self.button_Disconnect, 10, 1, 1, 1)
        self.items_grid.addWidget(self.bpm, 0, 0, 1, 2)

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

        self.ser.close()
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
        global k, i, N, cont_bpm

        if self.ser.is_open == True:
            while i < k:
                inicio_dato = self.ser.read(1)
                if inicio_dato == b'\x24':
                    dato_uart_byte = self.ser.read(5)
                    fin_dato = self.ser.read(1)
                    if fin_dato == b'\x23':
                        self.y_uart[i] = int.from_bytes(dato_uart_byte[0:4], byteorder='big', signed=True)
                        self.R_uart[i] = int.from_bytes(dato_uart_byte[4:], byteorder='big', signed=True)
                        cont_bpm = cont_bpm + 1
                        print([self.R_uart[i], cont_bpm])
                        if self.R_uart[i] == 1:
                            self.bpm.setText(str(int(60000 / cont_bpm)))
                            cont_bpm = 0

                        i = i + 1

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


            #print(str(60000/cont_bpm))




    def graficar(self,data):
        self.pcg = data
        self.time = np.arange(0, len(self.pcg), 1, dtype=np.float32)

        self.p1.plot(self.pcg, pen="r", symbol='o', symbolSize=5, symbolBrush="r")
        self.p1.showGrid(x=True, y=True, alpha=0.3)
        # self.p1.plot(data2, pen="g")



        # self.text = pg.TextItem(str(self.x_dl_5g_flag))
        # self.plt_1.addItem(self.text)
        # self.text.setPos(30, 20)


        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        self.vb = self.p1.vb
        self.p1.scene().sigMouseMoved.connect(self.mouseMoved)
        self.p1.scene().sigMouseClicked.connect(self.mouseClicked)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())