__author__      = "Niswatul Kariimah & Muhammad Masdar Mahasin"
__copyright__   = "Copyright Brawijaya University @2021"
__version__ = "0.0.1"
__license__ = "GPL"


# Import Library
import sys
import cv2 as cv
import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication

from PyQt5.uic import loadUi


import pyqtgraph as pg

class PyQtMainEntry(QMainWindow):
    def __init__(self):
        super().__init__()

        loadUi("E:/GUI_Sodiq_Monitoring.ui", self)

        self.camera = cv.VideoCapture(0)
        self.is_camera_opened = False  # Whether the camera has an open mark

        # Timer: 30ms capture a frame
        self._timer2 = QtCore.QTimer(self)
        self._timer2.timeout.connect(self._queryFrame)
        self._timer2.setInterval(50)


        self.tombolMulai.clicked.connect(self.btnOpenCamera_Clicked)
        self.tombolMulai_2.clicked.connect(self.btnCapture_Clicked)
        #self.btnReadImage.clicked.connect(self.btnReadImage_Clicked)
        #self.tombolMulai_3.clicked.connect(self.btnGray_Clicked)
        #self.btnThreshold.clicked.connect(self.btnThreshold_Clicked)

        self.comboBox.addItems(['Choose Filter',
                                'Sobel Kombinasi', 
                                'Canny',
                                'Laplacian'])

        #self.comboBox.currentIndexChanged.connect(self.tes_output)
        output = self.comboBox.currentText()
        #self.labelHistogram_2.setText(output)


    def btnOpenCamera_Clicked(self):
        '''
                 Turn the camera on and off
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.tombolMulai.setText("TURN OFF CAMERA")
            self._timer2.start()
        else:
            self.tombolMulai.setText("TURN ON CAMERA")
            self._timer2.stop()

    def btnCapture_Clicked(self):
        '''
                 Capture picture
        '''
        # The camera is not turned on, do not perform any operation
        
        if not self.is_camera_opened:
            return

        self.captured = self.frame

        # The following lines of code are almost the same, you can try to encapsulate it into a function
        rows, cols, channels = self.captured.shape
        bytesPerLine = channels * cols
        # When Qt displays pictures, it needs to be converted to QImgage type first
        QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
        self.labelHistogram.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelHistogram.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def btnReadImage_Clicked(self):
        '''
                 Read pictures from local
        '''
        # Open the file selection dialog
        filename,  _ = QFileDialog.getOpenFileName(self, 'Open picture')
        if filename:
            self.captured = cv.imread(str(filename))
            # OpenCV images are stored in BGR channel, and need to be changed from BGR to RGB when displayed
            self.captured = cv.cvtColor(self.captured, cv.COLOR_BGR2RGB)

            rows, cols, channels = self.captured.shape
            bytesPerLine = channels * cols
            QImg = QImage(self.captured.data, cols, rows, bytesPerLine, QImage.Format_RGB888)
            self.labelCapture.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelCapture.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
                 Loop to capture pictures
        '''
        ret, self.frame = self.camera.read()

        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv.cvtColor(self.frame, cv.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        output = self.comboBox.currentText()
        if output == 'Sobel Kombinasi':
            self.labelHistogram_2.setText('AAA')

            # Konversi citra RGB ke Gray
            self.cpatured = cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY)

            # Blur the image for better edge detection
            self.blur = cv.GaussianBlur(self.cpatured, (3,3), 0) 

            # Filter Sobel X-Y (edge detection)
            self.sobel_kombinasi = cv.Sobel(src=self.blur, ddepth=cv.CV_64F, dx=1, dy=0, ksize=0)
            self.sobel_kombinasi = np.uint8(np.absolute(self.sobel_kombinasi))

            rows, columns = self.sobel_kombinasi.shape
            bytesPerLine = columns

            # The grayscale image is a single channel, so Format_Indexed8 is needed
            QImg = QImage(self.sobel_kombinasi.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
            self.labelExtraction.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelExtraction.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif output == 'Canny':

            self.labelHistogram_2.setText('BBB')

            # Filter Canny
            self.canny = cv.Canny(self.frame, 100, 200)

            rows, columns = self.canny.shape
            bytesPerLine = columns

            # The grayscale image is a single channel, so Format_Indexed8 is needed
            QImg = QImage(self.canny.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
            self.labelExtraction.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelExtraction.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif output == 'Laplacian' :
            self.labelHistogram_2.setText('CCC')

            # Konversi citra RGB ke Gray
            self.cpatured = cv.cvtColor(self.frame, cv.COLOR_RGB2GRAY)

            # Filter Laplacian
            self.lap = cv.Laplacian(self.cpatured, cv.CV_64F, ksize=3)
            self.lap = np.uint8(np.absolute(self.lap))

            # Filter Canny
            self.canny = cv.Canny(self.frame, 100, 200)

            rows, columns = self.lap.shape
            bytesPerLine = columns

            # The grayscale image is a single channel, so Format_Indexed8 is needed
            QImg = QImage(self.lap.data, columns, rows, bytesPerLine, QImage.Format_Indexed8)
            self.labelExtraction.setPixmap(QPixmap.fromImage(QImg).scaled(
                self.labelExtraction.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())