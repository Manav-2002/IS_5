# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:30:38 2020

@author: satya
"""

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Matplotlib_pyqt5(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(Matplotlib_pyqt5, self).__init__(parent)

        # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setMinimumWidth(100)
        self.toolbar.setStyleSheet("QToolBar { border: 0px }")

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def plot(self,data):
        ''' plot some random stuff '''
        # random data

        # create an axis
        self.ax_plot = self.figure.add_subplot(111)

        # discards the old graph
        self.ax_plot.clear()

        # plot data
        self.ax_plot.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        
    def imshow(self,data):
        self.ax_image = self.figure.add_subplot(111) 
        self.ax_image.clear()
        self.ax_image.imshow(data)
        self.canvas.draw()
        
        
