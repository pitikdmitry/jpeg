import binascii


class BytesArray(list):

    def __init__(self, img_bytes):
        img_hex = binascii.hexlify(img_bytes)
        n = 2
        for i in range(0, len(img_hex), n):
            byte_hex = img_hex[i:i + n]
            super(BytesArray, self).append(byte_hex)

    def find_pair_index(self, str1: str, str2: str) -> int:
        str1 = bytes(str1, encoding="UTF-8")
        str2 = bytes(str2, encoding="UTF-8")

        for i in range(0, len(self)):
            if i + 1 < len(self):
                first_str = self[i]
                second_str = self[i + 1]
                s1 = first_str + second_str
                s2 = str1 + str2
                if first_str + second_str == str1 + str2:
                    return i
            else:
                return -1

        return -1
