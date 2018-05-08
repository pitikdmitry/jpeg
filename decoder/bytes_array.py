import binascii
from typing import Optional


class BytesArray(list):

    def __init__(self, img_bytes):
        img_hex = binascii.hexlify(img_bytes)
        n = 2
        for i in range(0, len(img_hex), n):
            byte_hex = img_hex[i:i + n]
            super(BytesArray, self).append(byte_hex)

    def find_pair(self, str1: str, str2: str, start: int = 0, end: int = -1) -> int:
        if end == -1:
            end = len(self)
        str1 = bytes(str1, encoding="UTF-8")
        str2 = bytes(str2, encoding="UTF-8")

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
        str1 = bytes(str1, encoding="UTF-8")
        str2 = bytes(str2, encoding="UTF-8")
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
