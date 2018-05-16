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
        self._y_blocks_amount = 0
        self._cb_blocks_amount = 0
        self._cr_blocks_amount = 0

        self._N = 8
        self._M = 8
        self._width_remainder = 0
        self._height_remainder = 0

        self._koef_cb = 0
        self._koef_cr = 0

        self._new_width = 0
        self._new_height = 0

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
        # self._height_remainder = height % self._N
        # if  self._height_remainder != 0:
        #     height = height - self._height_remainder + self._N
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, width: int):
        # self._width_remainder = width % self._N
        # if  self._width_remainder != 0:
        #     width = width - self._width_remainder + self._N
        self._width = width

    @property
    def channels_amount(self) -> int:
        return self._channels_amount

    @property
    def components(self) -> []:
        return self._components

    @channels_amount.setter
    def channels_amount(self, channels_amount: int):
        self._channels_amount = channels_amount

    def set_new_size(self):
        y_comp_index = 1
        y_component = self.get_component_by_id(y_comp_index)
        horizontal_blocks = y_component.horizontal_blocks
        vertical_blocks = y_component.vertical_blocks

        self._new_width = horizontal_blocks * self._N
        self._new_height = vertical_blocks * self._M

    def add_quantization_table(self, quantization_table: QuantizationTable):
        self._quantization_tables.append(quantization_table)

    def add_component(self, component: Component):
        self._components.append(component)

    def get_component_by_id(self, component_id: int) -> Component:
        for comp in self._components:
            if comp.component_id == component_id:
                return comp

    def get_quantization_table_by_id(self, table_id: int):
        for table in self._quantization_tables:
            if table.id == table_id:
                return table

    @property
    def quantization_tables(self) -> []:
        return self._quantization_tables

    @property
    def haffman_trees(self) -> []:
        return self._haffman_trees

    @property
    def y_channels_amount(self) -> int:
        return self._y_blocks_amount

    @property
    def cb_channels_amount(self) -> int:
        return self._cb_blocks_amount

    @property
    def cr_channels_amount(self) -> int:
        return self._cr_blocks_amount

    @property
    def koef_cb(self) -> int:
        return self._koef_cb

    @property
    def koef_cr(self) -> int:
        return self._koef_cr

    @property
    def new_width(self) -> int:
        return self._new_width

    @property
    def new_height(self) -> int:
        return self._new_height
