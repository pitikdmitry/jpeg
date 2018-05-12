import numpy as np

from decoder.utils.array_utils import get_array_from_list
from decoder.utils.quantization_table import QuantizationTable


class ImageInfo:
    def __init__(self):
        self._comment = ""
        self._width = 0
        self._height = 0
        self._channels_amount = 0
        self._quantization_tables = []
        self._haffman_trees = []
        self._y_channels = []
        self._cb_channels = []
        self._cr_channels = []

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comm: str):
        self._comment = comm

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def channels_amount(self) -> int:
        return self._channels_amount

    @channels_amount.setter
    def channels_amount(self, channels_amount: int):
        self._channels_amount = channels_amount

    def add_y_channel(self, l: []):
        arr = get_array_from_list(l)
        # arr = l
        self._y_channels.append(arr)

    def add_cb_channel(self, l: []):
        arr = get_array_from_list(l)
        # arr = l
        self._cb_channels.append(arr)

    def add_cr_channel(self, l: []):
        arr = get_array_from_list(l)
        # arr = l
        self._cr_channels.append(arr)

    def add_quantization_table(self, quantization_table: QuantizationTable):
        self._quantization_tables.append(quantization_table)

    def add_info_to_quantization_table(self, id: int, horizontal_thinning: int, vertical_thinning: int):
        for table in self._quantization_tables:
            if table.id == id:
                table.horizontal_thinning = horizontal_thinning
                table.vertical_thinning = vertical_thinning
                return

    @property
    def quantization_tables(self) -> []:
        return self._quantization_tables

    @property
    def haffman_trees(self) -> []:
        return self._haffman_trees

    @property
    def y_channels(self):
        return self._y_channels

    @property
    def cb_channels(self):
        return self._cb_channels

    @property
    def cr_channels(self):
        return self._cr_channels
