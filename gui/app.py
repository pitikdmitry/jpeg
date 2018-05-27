import sys
import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QToolTip, QFileDialog, QHBoxLayout, QLabel, \
    QDesktopWidget, QGridLayout, QWidget, QScrollArea, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, \
    QAbstractScrollArea
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
        self._grid_vertical_position = 0
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        scroll_area = QScrollArea()

        widget = QWidget()
        # Layout of Container Widget
        self._layout = QGridLayout()
        # self._layout = QVBoxLayout()
        widget.setLayout(self._layout)
        self.setCentralWidget(widget)

        # # Scroll Area Properties
        # scroll = QScrollArea()
        # # scroll.setVerticalScrollBarPolicy(ScrollBarAlwaysOn)
        # # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # scroll.setWidgetResizable(False)
        # scroll.setWidget(widget)
        #
        # # Scroll Area Layer add
        # vLayout = QVBoxLayout(self)
        # vLayout.addWidget(scroll)
        # self.setLayout(vLayout)

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
        while self._layout.itemAt(0) is not None:
            self._layout.itemAt(0).widget().setParent(None)
        self.show()

    def showDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', self._current_dir)[0]

        image, image_info = decode_image(file_name)
        self.show_image(image)
        self.show_image_info(image_info)

    def show_image(self, image):
        image_qt = QtGui.QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        pix = QtGui.QPixmap(image_qt)
        self._image_widget = QLabel(self)
        self._image_widget.setPixmap(pix)
        self._image_widget.setAlignment(QtCore.Qt.AlignCenter)
        self._layout.addWidget(self._image_widget, self._grid_vertical_position, 0)
        self._grid_vertical_position += 1

    def show_image_info(self, image_info):
        self.show_quantization_tables(image_info)

    def show_quantization_tables(self, image_info):
        tables = image_info.quantization_tables
        for i in range(0, len(tables)):
            table_label = QLabel("Quantization table id = " + str(tables[i].id))
            table_label.setAlignment(Qt.AlignCenter)
            self._layout.addWidget(table_label, self._grid_vertical_position, 0)
            self._grid_vertical_position += 1
            q_table = self.array_2_table(tables[i].table)
            self._layout.addWidget(q_table, self._grid_vertical_position, 0)
            self._grid_vertical_position += 1

    def array_2_table(self, array):
        table = QTableWidget()

        w = len(array)
        h = len(array[0])
        table.setColumnCount(w)
        table.setRowCount(h)
        for row in range(h):
            for column in range(w):
                table.setItem(row, column, QTableWidgetItem(str(array[row][column])))

        self.set_table_width_height(table, w, h)
        return table

    def set_table_width_height(self, table, w, h):
        column_width = 50
        column_height = 20
        table.verticalHeader().setDefaultSectionSize(column_height)
        table.horizontalHeader().setDefaultSectionSize(column_width)
        w_header = table.verticalHeader().sizeHint().width()
        h_header = table.horizontalHeader().sizeHint().height()
        table.setFixedWidth(w * column_width + 1.5 * w_header)
        table.setFixedHeight(h * column_height + 1.3 * h_header)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
