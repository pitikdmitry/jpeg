import binascii

from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException


def parse_ffd8(bytes_array: BytesArray):
    if bytes_array[0] + bytes_array[1] != b'ffd8':
        raise BadMarkerException


def parse_fffe(bytes_array: BytesArray):
    if bytes_array[2] + bytes_array[3] != b'fffe':
        raise BadMarkerException
    #   find ff db to cut comment
    ff_db_index = bytes_array.find_pair_index("ff", "db")
    if ff_db_index != -1:
        comment = bytes_array[4:ff_db_index]
        return


with open("favicon.jpg", "rb") as f:
    img = f.read()
    bytes_array = BytesArray(img)

    try:
        parse_ffd8(bytes_array)
        parse_fffe(bytes_array)
    except BadMarkerException as e:
        print("Bad marker exc")
