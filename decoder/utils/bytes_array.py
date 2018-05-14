import binascii


class BytesArray(list):

    def __init__(self, img_bytes):
        super(BytesArray, self).__init__()
        img_hex = binascii.hexlify(img_bytes)
        n = 2
        for i in range(0, len(img_hex), n):
            byte_hex = img_hex[i:i + n]
            string_hex = byte_hex.decode("utf-8")
            super(BytesArray, self).append(string_hex)

    def find_pair(self, str1: str, str2: str, start: int = 0, end: int = -1) -> int:
        if start >= len(self):
            return -1
        if end == -1:
            end = len(self)

        for i in range(start, end):
            if i + 1 < len(self):
                first_str = self[i]
                second_str = self[i + 1]
                if first_str + second_str == str1 + str2:
                    return i
            else:
                return -1

        return -1

    def find_all_pairs(self, str1: str, str2: str) -> []:
        result_arr = []

        for i in range(0, len(self)):
            if i + 1 < len(self):
                first_str = self[i]
                second_str = self[i + 1]
                if first_str + second_str == str1 + str2:
                    result_arr.append(i)

        if len(result_arr) > 0:
            return result_arr
        return -1

    def read_from_one_pair_to_other(self, pair1: str, pair2: str, start=0, end=-1):
        if start >= len(self):
            return -1
        if end == -1:
            end = len(self)

        start_index = -1
        end_index = -1
        start_found = False

        for i in range(start, end):
            if i + 1 < len(self):
                first_str = self[i]
                second_str = self[i + 1]
                if first_str + second_str == pair1:
                    start_index = i
                    start_found = True
                if first_str + second_str == pair2 and start_found:
                    end_index = i

        if start_index != -1 and end_index != -1:
            return self[start_index:end_index]

    def read_n_bytes(self, start_index: int, n: int) -> []:
        result_arr = []

        for i in range(start_index, start_index + n):
            if i < len(self):
                result_arr.append(self[i])
            else:
                break
        if len(result_arr) > 0:
            return result_arr
        return -1
