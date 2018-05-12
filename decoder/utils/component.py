class Component:
    def __init__(self, component_id: int, horizontal_thinning: int, vertical_thinning: int, quantization_table_id: int):
        self._component_id = component_id
        self._horizontal_thinning = horizontal_thinning
        self._vertical_thinning = vertical_thinning
        self._quantization_table_id = quantization_table_id

        self._dc_haff_table_id = -1
        self._ac_haff_table_id = -1

        self._array_of_blocks = []

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
