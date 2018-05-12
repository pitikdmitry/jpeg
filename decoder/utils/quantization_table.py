class QuantizationTable:
    def __init__(self, id: int, table: []):
        self._id = id

        for i in range(0, len(table)):
            for j in range(0, len(table[0])):
                table[i][j] = int(table[i][j], 16)

        self._table = table


    @property
    def id(self) -> int:
        return self._id

    @property
    def table(self) -> []:
        return self._table
