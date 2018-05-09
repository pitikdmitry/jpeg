from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException
from decoder.image_info import ImageInfo
from decoder.utils.haffman_tree import HaffmanTree
from decoder.utils.zig_zag import zig_zag_order


def parse_ffd8(bytes_array: BytesArray, image_info: ImageInfo):    #  заголовок
    if bytes_array[0] + bytes_array[1] != b'ffd8':
        raise BadMarkerException


def parse_fffe(bytes_array: BytesArray, image_info: ImageInfo):    #   комментарий
    if bytes_array[2] + bytes_array[3] != b'fffe':
        raise BadMarkerException
    #   find ff db to cut comment
    ff_db_index = bytes_array.find_pair("ff", "db")
    if ff_db_index != -1:
        comment = bytes_array[4:ff_db_index]
        image_info.comment = comment


def parse_ffdb(bytes_array: BytesArray, image_info: ImageInfo):     #   таблицы квантования
    ff_db_indexes = bytes_array.find_all_pairs("ff", "db")
    if ff_db_indexes == -1:
        raise BadMarkerException

    ff_c0_index = bytes_array.find_pair("ff", "c0")     #   ffc0 является правой границей для крайней таблицы квантования
    ff_db_indexes.append(ff_c0_index)

    for i in range(0, len(ff_db_indexes) - 1):    #   -1 для того чтобы +1 взять как верхнюю границу таблицы квантования т.е. ffc0
        header_index = ff_db_indexes[i] + 2
        start_index = ff_db_indexes[i] + 5  # первые два это сами ffdb, три заголовок
        end_index = ff_db_indexes[i + 1]
        header = bytes_array[header_index:header_index + 3]  # длина заголовока всегда 3 байта
        quantization_arr = bytes_array[start_index:end_index]
        quantization_table = zig_zag_order(quantization_arr)
        image_info.quantization_tables.append(quantization_table)


def parse_ffc0(bytes_array: BytesArray, image_info: ImageInfo): #   Информация о картинке(р - ры)
    pass


def parse_ffc4(bytes_array: BytesArray, image_info: ImageInfo):
    start_index = 0
    while True:
        haff_table_start = bytes_array.find_pair("ff", "c4", start=start_index) + 2
        header_length = 3
        ffc4_header = bytes_array.read_n_bytes(haff_table_start, header_length)
        haff_length = int(ffc4_header[1], 16)
        haff_arr = bytes_array.read_n_bytes(haff_table_start + header_length, haff_length - header_length)
        haff_tree = HaffmanTree(haff_arr)
        val1 = haff_tree.get_value("01")
        val2 = haff_tree.get_value("10")
        start_index = haff_table_start + haff_length


with open("favicon.jpg", "rb") as f:
    img = f.read()
    bytes_array = BytesArray(img)
    image_info = ImageInfo()    #   для результата
    try:
        parse_ffd8(bytes_array, image_info)
        parse_fffe(bytes_array, image_info)
        parse_ffdb(bytes_array, image_info)
        parse_ffc0(bytes_array, image_info)
        parse_ffc4(bytes_array, image_info)
    except BadMarkerException as e:
        print("Bad marker exc")
