import math

from decoder.exceptions.exceptions import BadThinningException


class Component:
    def __init__(self, component_id: int, horizontal_thinning: int, vertical_thinning: int, quantization_table_id: int,
                 image_width: int, image_height: int):
        self._component_id = component_id
        self._horizontal_thinning = horizontal_thinning
        self._vertical_thinning = vertical_thinning
        self._quantization_table_id = quantization_table_id
        self._image_width = image_width
        self._image_height = image_height

        self._dc_haff_table_id = -1
        self._ac_haff_table_id = -1

        self._blocks_amount = 0
        self._array_of_blocks = []
        self._N = 8
        self._M = 8
        self.count_blocks()

    def count_blocks(self):
        if self._image_width % self._N != 0:
            raise BadThinningException
            # self._y_channels_amount += 1
        if self._image_height % self._M != 0:
            raise BadThinningException

        self._blocks_amount = (self._image_width / self._N) * (self._horizontal_thinning ** 2) + \
                              (self._image_height / self._M) * (self.vertical_thinning ** 2)
        self._blocks_amount /= 4
        if not self._is_int(self._blocks_amount):
            pass
            # raise BadThinningException
        self._blocks_amount = math.floor(self._blocks_amount)

    def _is_int(self, n):
        return int(n) == float(n)

    def substract_dc(self):
        if self._blocks_amount <= 0:
            return

        dc_koef_prev = self._array_of_blocks[0][0][0]
        for i in range(1, self._blocks_amount):
            dc_koef_current = self._array_of_blocks[i][0][0]
            dc_koef_current = dc_koef_prev + dc_koef_current
            dc_koef_prev = dc_koef_current
            self._array_of_blocks[i][0][0] = dc_koef_current

    @property
    def component_id(self) -> int:
        return self._component_id

    @property
    def quantization_table_id(self) -> int:
        return self._quantization_table_id

    @property
    def horizontal_thinning(self) -> int:
        return self._horizontal_thinning

    @property
    def vertical_thinning(self) -> int:
        return self._vertical_thinning

    @property
    def dc_haff_table_id(self) -> int:
        return self._dc_haff_table_id

    @property
    def ac_haff_table_id(self) -> int:
        return self._ac_haff_table_id

    @ac_haff_table_id.setter
    def ac_haff_table_id(self, id: int):
        self._ac_haff_table_id = id

    @dc_haff_table_id.setter
    def dc_haff_table_id(self, id: int):
        self._dc_haff_table_id = id

    @property
    def array_of_blocks(self) -> []:
        return self._array_of_blocks

    @property
    def blocks_amount(self) -> int:
        return self._blocks_amount


