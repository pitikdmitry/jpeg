import numpy as np

from decoder.utils.array_utils import get_array_from_list


class ImageInfo:
    def __init__(self):
        self._comment = ""
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

    def add_quantization_table(self, l: []):
        for i in range(0, len(l)):
            for j in range(0, len(l[0])):
                l[i][j] = int(l[i][j], 16)

        res = np.asarray(l, dtype=int)
        self._quantization_tables.append(res)

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
