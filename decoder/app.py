import binascii

from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException


def parse_ffd8(img):
    if img[0:4] != b'ffd8':
        raise BadMarkerException
    print(img[0:4])


def parse_fffe(img):
    pass


with open("favicon.jpg", "rb") as f:
    img = f.read()
    bytes_array = BytesArray(img)

    try:
        parse_ffd8(img)
    except BadMarkerException as e:
        print("Bad marker exc")
