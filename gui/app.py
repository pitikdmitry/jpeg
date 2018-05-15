import sys
import os
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QToolTip, QFileDialog
from PyQt5.QtGui import QIcon, QFont


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        openFileAction = QAction(QIcon('upload-icon.png'), 'Upload image', self)
        openFileAction.setStatusTip('Uploading image')
        openFileAction.triggered.connect(self.showDialog)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(openFileAction)

        self.setGeometry(800, 600, 1000, 1000)
        self.setWindowTitle('Jpeg reader')
        self.setWindowIcon(QIcon('title_icon.png'))
        self.show()

    def showDialog(self):
        current_dir = os.getcwd()
        fname = QFileDialog.getOpenFileName(self, 'Open file', current_dir)[0]

        f = open(fname, 'r')

        with f:
            data = f.read()
            self.textEdit.setText(data)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
