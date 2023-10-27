import numpy as np
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,
QLineEdit, QCheckBox, QTextEdit, QGridLayout,QPushButton,QFileDialog, QTableWidget, QTableWidgetItem,QProgressBar)
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

        self.pcg=[]
        self.preds = []
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.label = pg.LabelItem(justify='right')
        self.win.addItem(self.label)
        #self.r = pg.PolyLineROI([(0, 0), (10, 10)])



        self.p1 =self.win.addPlot(row=0, col=0)
        # customize the averaged curve that can be activated from the context menu:
        self.p1.avgPen = pg.mkPen('#FFFFFF')
        self.p1.avgShadowPen = pg.mkPen('#8080DD', width=10)
        #self.p1.addItem(self.r)




        self.bpm= QLabel("",self)


        self.button_Connect = QPushButton("Connect",self)
        self.button_Connect.clicked.connect(self.buttonConnectClicked)
        self.button_Disconnect = QPushButton("Disconnect",self)
        self.button_Disconnect.clicked.connect(self.buttonDisconnectClicked)


        #self.table = QTableWidget(4,2)

        self.items_grid = QGridLayout()
        self.items_grid.addWidget(self.win , 0, 1, 5,1)
        self.items_grid.addWidget(self.button_Connect, 0, 0, 1,1)
        self.items_grid.addWidget(self.button_Disconnect, 2, 0, 1, 1)
        self.items_grid.addWidget(self.bpm, 3, 0, 1, 1)



        self.setLayout(self.items_grid)



    def buttonConnectClicked(self, evt):

        pass


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