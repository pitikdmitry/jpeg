import binascii


class BytesArray(list):

    def __init__(self, img_bytes):
        img_hex = binascii.hexlify(img_bytes)
        n = 2
        for i in range(0, len(img_hex), n):
            byte_hex = img_hex[i:i + n]
            super(BytesArray, self).append(byte_hex)
