import sys
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QToolTip, QFileDialog, QHBoxLayout, QLabel, \
    QDesktopWidget
from PyQt5.QtGui import QIcon, QFont, QPixmap, QImage

from decoder.app import decode_image


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        # hbox = QHBoxLayout(self)

        #   toolbar
        openFileAction = QAction(QIcon('upload-icon.png'), 'Upload image', self)
        openFileAction.setStatusTip('Uploading image')
        openFileAction.triggered.connect(self.showDialog)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(openFileAction)

        #   all window
        self.setGeometry(800, 600, 1000, 1000)
        self.setWindowTitle('Jpeg reader')
        self.setWindowIcon(QIcon('upload-icon.png'))

        #
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showDialog(self):
        current_dir = os.getcwd()
        file_name = QFileDialog.getOpenFileName(self, 'Open file', current_dir)[0]

        image = decode_image(file_name)
        self.show_image(image)

    def show_image(self, image):
        image_qt = QtGui.QImage(image.data, image.shape[0], image.shape[1], QImage.Format_RGB888)
        pix = QtGui.QPixmap(image_qt)
        lbl = QLabel(self)
        lbl.setPixmap(pix)
        self.setCentralWidget(lbl)
        if image.
        self.setGeometry(800, 600, image.shape[0], image.shape[1])
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
