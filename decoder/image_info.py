class ImageInfo:
    def __init__(self):
        self._comment = ""
        self._quantization_tables = []
        self._haffman_trees = []

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comm: str):
        self._comment = comm

    @property
    def quantization_tables(self) -> []:
        return self._quantization_tables

    @property
    def haffman_trees(self) -> []:
        return self._haffman_trees
