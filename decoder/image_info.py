class ImageInfo:
    def __init__(self):
        self.comment_str = ""
        self.quantization_tables = []

    @property
    def comment(self) -> str:
        return self.comment

    @comment.setter
    def comment(self, comm: str):
        self.comment_str = comm

    # @property
    # def quantization_tables(self) -> []:
    #     return self.quantization_tables
