import sys
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QToolTip, QFileDialog, QHBoxLayout, QLabel, \
    QDesktopWidget, QGridLayout, QWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage

from decoder.app import decode_image


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self._current_dir = os.getcwd()
        self._window_width = 1280
        self._window_height = 1024
        self._basic_offset = 500
        self._layout = None
        self._image_widget = None
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        # hbox = QHBoxLayout(self)
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self._layout = QGridLayout(self)
        centralWidget.setLayout(self._layout)
        # centralWidget.setLayout(gridLayout)

        #   toolbar
        openFileAction = QAction(QIcon('upload-icon.png'), 'Upload image', self)
        openFileAction.setStatusTip('Uploading image')
        openFileAction.triggered.connect(self.showDialog)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(openFileAction)

        closeFileAction = QAction(QIcon('cross.png'), 'Close file', self)
        closeFileAction.setStatusTip('Closing file')
        closeFileAction.triggered.connect(self.close_image)

        toolbar.addAction(closeFileAction)
        #   all window
        self.setGeometry(self._basic_offset, self._basic_offset, self._window_width, self._window_height)
        self.setWindowTitle('Jpeg reader')
        self.setWindowIcon(QIcon(self._current_dir + '/title_icon.svg'))

        #
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_image(self):
        self._layout.itemAt(0).widget().setParent(None)
        self.show()

    def showDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', self._current_dir)[0]

        image = decode_image(file_name)
        self.show_image(image)

    def show_image(self, image):
        image_qt = QtGui.QImage(image.data, image.shape[0], image.shape[1], QImage.Format_RGB888)
        pix = QtGui.QPixmap(image_qt)
        self._image_widget = QLabel(self)
        self._image_widget.setPixmap(pix)
        self._image_widget.setAlignment(QtCore.Qt.AlignCenter)
        self._layout.addWidget(self._image_widget, 0, 0)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
