import os
import numpy as np
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QToolTip, QFileDialog, QHBoxLayout, QLabel, \
    QDesktopWidget, QWidget
from PyQt5.QtGui import QIcon, QFont, QImage

from decoder.app import decode_image
from gui.tree_utils import TreeUtils


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self._current_dir = os.getcwd()
        self._window_width = 1280
        self._window_height = 1024
        self._basic_offset = 500
        self._layout = None
        self._image_widget = None
        self._main_widget = None
        self._grid_vertical_position = 0
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self._main_widget = QWidget()
        self._layout = QHBoxLayout()
        self._main_widget.setLayout(self._layout)
        self.setCentralWidget(self._main_widget)

        #   toolbar
        open_file_action = QAction(QIcon(self._current_dir + '/gui_images/upload-icon.png'), 'Upload image', self)
        open_file_action.setStatusTip('Uploading image')
        open_file_action.triggered.connect(self.show_dialog)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(open_file_action)

        close_file_action = QAction(QIcon(self._current_dir + '/gui_images/cross.png'), 'Close file', self)
        close_file_action.setStatusTip('Closing file')
        close_file_action.triggered.connect(self.close_image)

        toolbar.addAction(close_file_action)
        self.setGeometry(self._basic_offset, self._basic_offset, self._window_width, self._window_height)
        self.setWindowTitle('Jpeg reader')
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def close_image(self):
        while self._layout.itemAt(0) is not None:
            self._layout.itemAt(0).widget().setParent(None)
        self.show()

    def show_dialog(self):
        self.close_image()
        file_name = QFileDialog.getOpenFileName(self, 'Open file', self._current_dir + "/test_images/")[0]

        image, image_info = decode_image(file_name)
        self.show_image(image)
        self.show_quantization_tables(image_info)
        self.print_tree_in_file(image_info)

    def show_image(self, image):
        image_qt = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pix = QtGui.QPixmap(image_qt)
        self._image_widget = QLabel(self)
        self._image_widget.setPixmap(pix)
        self._image_widget.setAlignment(QtCore.Qt.AlignCenter)
        self._layout.addWidget(self._image_widget, self._grid_vertical_position)
        self._grid_vertical_position += 1

    def show_quantization_tables(self, image_info):
        tables = image_info.quantization_tables
        for i in range(0, len(tables)):
            self.print_table_in_file(tables[i])

    def print_table_in_file(self, table):
        table_id = table.id
        file_name = self._current_dir + "/quantization_tables/table_" + str(table_id) + ".txt"
        f = open(file_name, 'w')
        np.savetxt(file_name, table.table, fmt='%1.0f', delimiter='\t')
        f.close()

    def print_tree_in_file(self, image_info):
        haff_trees = image_info.haffman_trees
        for i in range(0, len(haff_trees)):
            tree_utils = TreeUtils()
            tree = haff_trees[i]
            tree_utils.save_tree(tree)


if __name__ == '__main__':

    app = QApplication([])
    ex = Example()
    app.exec_()
