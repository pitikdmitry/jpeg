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
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self._layout = QGridLayout(self)
        central_widget.setLayout(self._layout)

        #   toolbar
        open_file_action = QAction(QIcon('upload-icon.png'), 'Upload image', self)
        open_file_action.setStatusTip('Uploading image')
        open_file_action.triggered.connect(self.showDialog)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(open_file_action)

        close_file_action = QAction(QIcon('cross.png'), 'Close file', self)
        close_file_action.setStatusTip('Closing file')
        close_file_action.triggered.connect(self.close_image)

        toolbar.addAction(close_file_action)
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
        image_qt = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pix = QtGui.QPixmap(image_qt)
        self._image_widget = QLabel(self)
        self._image_widget.setPixmap(pix)
        self._image_widget.setAlignment(QtCore.Qt.AlignCenter)
        self._layout.addWidget(self._image_widget, 0, 0)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
