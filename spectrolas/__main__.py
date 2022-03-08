#!/usr/bin/env python3

from seabreeze.spectrometers import Spectrometer
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
import time
import sys
import numpy as np
import colorpy

class Application(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([''])
        self.window = QtWidgets.QMainWindow()
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(QtWidgets.QVBoxLayout())
        self.window.setCentralWidget(self.main_widget)
        
        self.figure = plt.figure(figsize=(12, 8))
        self.nav = NavigationToolbar2QT(self.figure.canvas, self.main_widget)
        self.main_widget.layout().addWidget(self.nav)
        self.ax = self.figure.add_subplot()
        self.main_widget.layout().addWidget(self.figure.canvas)
        self.bbox = self.figure.canvas.copy_from_bbox(self.figure.bbox)
        self.figure.canvas.mpl_connect('resize_event', self.onResize)
        self.figure.canvas.mpl_connect('draw_event', self.onDraw)
        
        self.spec = Spectrometer.from_first_available()
        self.spec.integration_time_micros(100000)
        
        self.bkgBtn = QtWidgets.QPushButton('Record Background')
        self.bkgBtn.pressed.connect(self.recordBkg)
        self.main_widget.layout().addWidget(self.bkgBtn)
        
        # self.line, = self.ax.plot(self.spec.wavelengths(), self.spec.intensities())
        self.lines = []
        self.intensities = self.spec.intensities()
        self.wavelengths = self.spec.wavelengths()
        self.bin_size = 5
        minimum_value = min(self.intensities)
        for i in range(int(len(self.intensities) / self.bin_size)):
            first_index = i * self.bin_size
            last_index = (i + 1) * self.bin_size
            
            x = sum(self.wavelengths[first_index:last_index]) / len(self.wavelengths[first_index:last_index])
            y = sum(self.intensities[first_index:last_index]) / len(self.intensities[first_index:last_index])
            self.lines.append(self.ax.plot(
                [x, x],
                [minimum_value, y],
                color=wavelength_to_rgb(x),
                linewidth=3)[0])
            
        self.background = np.zeros(len(self.spec.wavelengths()))
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(40)
        self.timer.timeout.connect(self.update)
        self.t0 = time.time()
        self.ax.set_xlim((380, 850)) 
        self.window.show()
        self.figure.canvas.draw()
        self.timer.start()
        sys.exit(self.exec_())
        
    def recordBkg(self):
        self.background = self.spec.intensities()
        
    def update_plot(self):
        intensities = self.spec.intensities() - self.background
        self.line.set_ydata(intensities)
        self.ax.set_ylim(min(intensities), max(intensities))
        self.figure.canvas.draw_idle()
        
    def update(self):
        intensities = self.spec.intensities() - self.background
        minimum_value = min(intensities)
        self.ax.set_ylim(0, max(intensities))
        for i in range(int(len(intensities) / self.bin_size)):
            first_index = i * self.bin_size
            last_index = (i + 1) * self.bin_size
            y = sum(intensities[first_index:last_index]) / len(intensities[first_index:last_index])
            self.lines[i].set_ydata([minimum_value, y])
        self.figure.canvas.draw_idle()
        
    def onResize(self, _):
        self.figure.canvas.draw()
        
    def onDraw(self, _):
        pass
        # self.bbox = self.figure.canvas.copy_from_bbox(self.figure.bbox)
        
        
        
def wavelength_to_rgb(wavelength, gamma=0.8):

    '''This converts a given wavelength of light to an 
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif wavelength >= 440 and wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif wavelength >= 490 and wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif wavelength >= 510 and wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif wavelength >= 580 and wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif wavelength >= 645 and wavelength <= 750:
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    return np.array((R, G, B))

if __name__ == "__main__":
    app = Application()
        
