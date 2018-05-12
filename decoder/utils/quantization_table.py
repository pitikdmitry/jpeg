class QuantizationTable:
    def __init__(self, id: int, table: []):
        self._id = id

        for i in range(0, len(table)):
            for j in range(0, len(table[0])):
                table[i][j] = int(table[i][j], 16)

        self._table = table
        self._horizontal_thinning = -1
        self._vertical_thinning = -1

    @property
    def id(self) -> int:
        return self._id

    @property
    def table(self) -> []:
        return self._table

    @property
    def horizontal_thinning(self) -> int:
        return self._horizontal_thinning

    @horizontal_thinning.setter
    def horizontal_thinning(self, horizontal_thinning: int):
        self._horizontal_thinning = horizontal_thinning

    @property
    def vertical_thinning(self) -> int:
        return self._vertical_thinning

    @vertical_thinning.setter
    def vertical_thinning(self, vertical_thinning: int):
        self._vertical_thinning = vertical_thinning
