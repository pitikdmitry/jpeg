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

    @property
    def components(self) -> []:
        return self._components

    @channels_amount.setter
    def channels_amount(self, channels_amount: int):
        self._channels_amount = channels_amount

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
