import numpy as np

from decoder.utils.array_utils import get_array_from_list
from decoder.utils.component import Component
from decoder.utils.quantization_table import QuantizationTable


class ImageInfo:
    def __init__(self):
        self._comment = ""
        self._width = 0
        self._height = 0
        self._channels_amount = 0
        self._quantization_tables = []
        self._components = []
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

    def add_component(self, component: Component):
        self._components.append(component)

    def add_info_to_component(self, component_id: int, dc_table_id: int, ac_table_id: int):
        for comp in self._components:
            if comp.component_id == component_id:
                comp.dc_haff_table_id = dc_table_id
                comp.ac_haff_table_id = ac_table_id

    def get_component_by_id(self, component_id: int) -> Component:
        for comp in self._components:
            if comp.component_id == component_id:
                return comp

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
