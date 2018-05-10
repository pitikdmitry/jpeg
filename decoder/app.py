from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException, BadDecodeException
from decoder.image_info import ImageInfo
from decoder.utils.array_utils import create_zeros_list
from decoder.utils.haffman_tree import HaffmanTree
from decoder.utils.zig_zag import ZigZag


def parse_ffd8(bytes_array: BytesArray, image_info: ImageInfo):    #  заголовок
    if bytes_array[0] + bytes_array[1] != 'ffd8':
        raise BadMarkerException


def parse_fffe(bytes_array: BytesArray, image_info: ImageInfo):    #   комментарий
    if bytes_array[2] + bytes_array[3] != 'fffe':
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
    zig_zag = ZigZag()

    for i in range(0, len(ff_db_indexes) - 1):    #   -1 для того чтобы +1 взять как верхнюю границу таблицы квантования т.е. ffc0
        header_index = ff_db_indexes[i] + 2
        start_index = ff_db_indexes[i] + 5  # первые два это сами ffdb, три заголовок
        end_index = ff_db_indexes[i + 1]
        header = bytes_array[header_index:header_index + 3]  # длина заголовока всегда 3 байта
        quantization_arr = bytes_array[start_index:end_index]
        quantization_table = zig_zag.zig_zag_order(quantization_arr)
        image_info.quantization_tables.append(quantization_table)


def parse_ffc0(bytes_array: BytesArray, image_info: ImageInfo): #   Информация о картинке(р - ры)
    pass


def parse_ffc4(bytes_array: BytesArray, image_info: ImageInfo): #   haffman
    start_index = 0
    while True:
        haff_table_start = bytes_array.find_pair("ff", "c4", start=start_index)
        if haff_table_start == -1:
            break
        haff_table_start += 2
        header_length = 3
        ffc4_header = bytes_array.read_n_bytes(haff_table_start, header_length)
        haff_length = int(ffc4_header[0] + ffc4_header[1], 16)  # changed
        ac_dc_id = ffc4_header[2]
        haff_arr = bytes_array.read_n_bytes(haff_table_start + header_length, haff_length - header_length)
        haff_tree = HaffmanTree(haff_arr, ac_dc_id)
        # val0 = haff_tree.get_value("100")
        # val1 = haff_tree.get_value("101")
        # val2 = haff_tree.get_value("1100")
        # val3 = haff_tree.get_value("1101")
        # val4 = haff_tree.get_value("1110")
        # val5 = haff_tree.get_value("11110")

        image_info.haffman_trees.append(haff_tree)
        start_index = haff_table_start + haff_length


def parse_ffda(bytes_array: BytesArray, image_info: ImageInfo): # start of scan
    ffda_data = bytes_array.read_from_one_pair_to_other("ffda", "ffd9")
    header_length = int(ffda_data[2] + ffda_data[3], 16)   #   в первых ьдвух байтах длина только для заголовочной части а не для всей секции
    ffc4_header = ffda_data[4: header_length]
    amount_of_components = int(ffc4_header[0], 16)
    coded_data = ffda_data[(header_length + 2):]
    coded_data_str = ""
    for ch in coded_data:
        coded_data_str += ch
    ch_10 = int(coded_data_str, 16)
    ch_2 = bin(ch_10)
    coded_data_binary = ch_2[2:]

    #   в цикле для количества компонентов считываем по 2 байта(информацию о них)
    arr_for_index = [0]
    if amount_of_components == 3:
        y_info = ffda_data[5:7]
        for i in range(0, 4):
            zig_zag = ZigZag()
            res_y_arr = parse_channel(coded_data_binary, y_info, image_info, zig_zag, arr_for_index)
        cb_info = ffda_data[7:9]
        zig_zag = ZigZag()
        res_cb_arr = parse_channel(coded_data_binary, y_info, image_info, zig_zag, arr_for_index)
        zig_zag = ZigZag()
        cr_info = ffda_data[9:11]
        res_cr_arr = parse_channel(coded_data_binary, y_info, image_info, zig_zag, arr_for_index)
    elif amount_of_components == 1:
        y_info = ffda_data[5:7]
        zig_zag = ZigZag()
        res_y_arr = parse_channel(coded_data_binary, y_info, image_info, zig_zag)


def parse_channel(code: str, y_info: str, image_info: ImageInfo, zig_zag: ZigZag, arr_for_index: []):
    result_array = create_zeros_list(8, 8)
    haffman_trees = image_info.haffman_trees
    dc_haff_tree = None
    ac_haff_tree = None

    y_dc_table_num = int(y_info[1][0])
    y_ac_table_num = int(y_info[1][1])
    for tree in haffman_trees:
        if int(tree.ac_dc_id[1]) == y_dc_table_num:
            if int(tree.ac_dc_id[0]) == 0:
                dc_haff_tree = tree

        if int(tree.ac_dc_id[1]) == y_ac_table_num:
            if int(tree.ac_dc_id[0]) == 1:
                ac_haff_tree = tree

    #   reading dc
    dc = dc_haff_tree.get_next_value(code, arr_for_index)
    dc_koef = 0
    if dc.value == "root" or dc.value == "node":
        raise BadDecodeException
    if dc.value != "0":
        dc_koef = dc_haff_tree.get_next_n_bits(code, arr_for_index, int(dc.value))
        if dc_koef[0] != "1":
            dc_koef = int(dc_koef, 2) - 2 ** int(dc.value) + 1
        else:
            dc_koef = int(dc_koef, 2)
    zig_zag.put_in_zig_zag(result_array, dc_koef)
    #   reading ac
    ac = ac_haff_tree.get_next_value(code, arr_for_index)
    while True:
        if ac.value == "root" or ac.value == "node":
            image_info.y_channels.append(result_array)
            return result_array

        amount_zeros = int(ac.value[0])
        for i in range(0, amount_zeros):
            zig_zag.put_in_zig_zag(result_array, 0)

        length_of_koef = int(ac.value[1])
        if length_of_koef == 0:
            return result_array
            # ac = ac_haff_tree.get_next_value(code, arr_for_index)
            # continue    # may be need to add 0
        ac_koef = ac_haff_tree.get_next_n_bits(code, arr_for_index, length_of_koef)
        if ac_koef[0] != "1":
            a = int(ac_koef, 2)
            c = int(ac.value[1])
            b = 2 ** int(ac.value[1])
            ac_koef = int(ac_koef, 2) - 2 ** int(ac.value[1]) + 1
        else:
            ac_koef = int(ac_koef, 2)
        zig_zag.put_in_zig_zag(result_array, ac_koef)
        ac = ac_haff_tree.get_next_value(code, arr_for_index)


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
        parse_ffda(bytes_array, image_info)
    except BadMarkerException as e:
        print("Bad marker exc")
# даюовить проверку что заполнили всю матрицу
