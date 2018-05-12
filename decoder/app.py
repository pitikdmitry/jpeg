import numpy as np
from skimage.io import imshow
from matplotlib import pyplot as plt

from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException, BadDecodeException, BadDimensionException, \
    BadChannelsAmountException, BadQuantizationValuesLength, BadComponentsAmountException, LengthToReadZeroException
from decoder.utils.component import Component
from decoder.utils.image_info import ImageInfo
from decoder.utils.array_utils import create_zeros_list, append_right, append_down, multiply_2d_matrixes
from decoder.utils.dct import idct
from decoder.utils.haffman_tree import HaffmanTree
from decoder.utils.quantization_table import QuantizationTable
from decoder.utils.zig_zag import ZigZag


SECTION_TITLE_SIZE = 2
N = 8   #   rows
M = 8   #   cols


def parse_ffd8(bytes_array: BytesArray):    #  заголовок
    ff_d8_start = 0
    if bytes_array[ff_d8_start] + bytes_array[ff_d8_start + 1] != 'ffd8':
        raise BadMarkerException


def parse_fffe(bytes_array: BytesArray, image_info: ImageInfo):    #   комментарий
    ff_ee_start = 2
    if bytes_array[ff_ee_start] + bytes_array[ff_ee_start + 1] != 'fffe':
        raise BadMarkerException

    ff_ee_header_size = 2
    comment = bytes_array.read_n_bytes(ff_ee_start + SECTION_TITLE_SIZE, ff_ee_header_size)
    comment = comment[2:]
    image_info.comment = comment


def parse_ffdb(bytes_array: BytesArray, image_info: ImageInfo):     #   таблицы квантования
    ff_db_indexes = bytes_array.find_all_pairs("ff", "db")
    if ff_db_indexes == -1:
        raise BadMarkerException

    header_size = 3
    zig_zag = ZigZag()
    for ff_db_index in ff_db_indexes:
        ff_db_index += SECTION_TITLE_SIZE
        header = bytes_array[ff_db_index: ff_db_index + header_size]
        ff_db_size = int(header[0] + header[1], 16)

        ff_db_data = bytes_array[ff_db_index: ff_db_index + ff_db_size]
        ff_db_data_index = 0
        values_length = int(ff_db_data[ff_db_data_index + 2][0], 16)
        if values_length != 0:
            raise BadQuantizationValuesLength

        quantization_table_id = int(ff_db_data[ff_db_data_index + 2][1], 16)

        quantization_table_index = ff_db_data_index + 3
        quantization_arr = ff_db_data[quantization_table_index:]
        quantization_table = zig_zag.zig_zag_order(quantization_arr)
        image_info.add_quantization_table(QuantizationTable(quantization_table_id, quantization_table))


def parse_ffc0(bytes_array: BytesArray, image_info: ImageInfo): #   Информация о картинке(р - ры)
    ff_c0_index = bytes_array.find_pair("ff", "c0")

    header_index = ff_c0_index + SECTION_TITLE_SIZE
    ff_db_size = int(bytes_array[header_index] + bytes_array[header_index + 1], 16)
    ff_c0_data = bytes_array[header_index: header_index + ff_db_size]
    ff_db_data_index = 0
    channel_dimension = int(ff_c0_data[ff_db_data_index + 2], 16)
    if channel_dimension != 8:
        raise BadDimensionException

    image_size_index = ff_db_data_index + 3

    image_height = int(ff_c0_data[image_size_index] + ff_c0_data[image_size_index + 1], 16)
    image_width = int(ff_c0_data[image_size_index + 2] + ff_c0_data[image_size_index + 3], 16)
    image_info.width = image_width
    image_info.height = image_height

    channels_amount_index = ff_db_data_index + 7
    channels_amount = int(ff_c0_data[channels_amount_index], 16)
    if channels_amount != 3:
        raise BadChannelsAmountException
    image_info.channels_amount = channels_amount

    channel_data_size = 3
    channel_info_index = channels_amount_index + 1
    for i in range(0, channels_amount):
        channel_data = ff_c0_data[channel_info_index: channel_info_index + channel_data_size]
        component_id = int(channel_data[0], 16)
        horizontal_thinning = int(channel_data[1][0], 16)
        vertical_thinning = int(channel_data[1][1], 16)
        quantization_table_id = int(channel_data[2], 16)
        image_info.add_component(Component(component_id, horizontal_thinning, vertical_thinning, quantization_table_id, image_info.width, image_info.height))

        channel_info_index += 3


def parse_ffc4(bytes_array: BytesArray, image_info: ImageInfo): #   haffman
    ff_c4_indexes = bytes_array.find_all_pairs("ff", "c4")
    if ff_c4_indexes == -1:
        raise BadMarkerException

    for ff_c4_index in ff_c4_indexes:
        ff_c4_index += 2
        ff_c4_length = int(bytes_array[ff_c4_index] + bytes_array[ff_c4_index + 1], 16)
        ffc4_data = bytes_array[ff_c4_index: ff_c4_index + ff_c4_length]
        ff_c4_data_index = 0

        ac_dc_class = int(ffc4_data[2][0], 16)
        haff_table_id = int(ffc4_data[2][1], 16)

        haff_amount_length = 16
        haff_amount_start = ff_c4_data_index + 3
        haff_amount_arr = ffc4_data[haff_amount_start: haff_amount_start + haff_amount_length]

        haff_values_start = haff_amount_start + haff_amount_length
        haff_value_arr = ffc4_data[haff_values_start:]
        haff_tree = HaffmanTree(haff_amount_arr, haff_value_arr, ac_dc_class, haff_table_id)
        # val0 = haff_tree.get_value("100")
        # val1 = haff_tree.get_value("101")
        # val2 = haff_tree.get_value("1100")
        # val3 = haff_tree.get_value("1101")
        # val4 = haff_tree.get_value("1110")
        # val5 = haff_tree.get_value("11110")

        image_info.haffman_trees.append(haff_tree)


def parse_ffda(bytes_array: BytesArray, image_info: ImageInfo): # start of scan
    ffda_data = bytes_array.read_from_one_pair_to_other("ffda", "ffd9")
    header_length = int(ffda_data[2] + ffda_data[3], 16)   #   в первых ьдвух байтах длина только для заголовочной части а не для всей секции

    ffc4_header_data = ffda_data[SECTION_TITLE_SIZE: header_length]
    ffc4_header_index = 0
    amount_of_components = int(ffc4_header_data[ffc4_header_index + 2], 16)
    if amount_of_components != 3:
        raise BadComponentsAmountException

    # берем данные и переводим в двоичную строку(0111010...)
    coded_data = ffda_data[(header_length + 2):]
    coded_data_str = ""
    for ch in coded_data:
        coded_data_str += ch
    ch_10 = int(coded_data_str, 16)
    ch_2 = bin(ch_10)
    coded_data_binary = ch_2[2:]

    components_index = ffc4_header_index + 3
    arr_for_index = [0]

    for i in range(0, amount_of_components):
        component_id = int(ffc4_header_data[components_index], 16)
        dc_table_id = int(ffc4_header_data[components_index + 1][1])
        ac_table_id = int(ffc4_header_data[components_index + 1][0])

        component = image_info.get_component_by_id(component_id)
        component.dc_haff_table_id = dc_table_id
        component.ac_haff_table_id = ac_table_id

        for i in range(0, component.blocks_amount):
            parse_channel(coded_data_binary, component, image_info, arr_for_index)

        components_index += 2


def parse_channel(code: str, component: Component, image_info: ImageInfo, arr_for_index: []):
    result_array = create_zeros_list(N, M)
    zig_zag = ZigZag()
    dc_haff_tree = None
    ac_haff_tree = None

    for tree in image_info.haffman_trees:
        if tree.ac_dc_class == 0 and tree.haff_table_id == component.dc_haff_table_id: # если таблица для dc и если совпадает id
            dc_haff_tree = tree

        if tree.ac_dc_class == 1 and tree.haff_table_id == component.ac_haff_table_id: # если таблица для ac и если совпадает id
            ac_haff_tree = tree

    #   reading dc
    dc = dc_haff_tree.get_next_value(code, arr_for_index)
    dc_koef = 0
    if dc.value == "root" or dc.value == "node":
        raise BadDecodeException
    if dc.value != "0" and dc.value != "00":
        length_to_read = int(dc.value)
        if length_to_read == 0:
            raise LengthToReadZeroException
        dc_koef = dc_haff_tree.get_next_n_bits(code, arr_for_index, length_to_read)
        if dc_koef[0] != "1":
            dc_koef = int(dc_koef, 2) - 2 ** length_to_read + 1
        else:
            dc_koef = int(dc_koef, 2)
    zig_zag.put_in_zig_zag(result_array, dc_koef)

    #   reading ac
    ac = ac_haff_tree.get_next_value(code, arr_for_index)
    while True:
        if ac.value == "root" or ac.value == "node" or ac.value == "00" or ac.value == "0":
            component.array_of_blocks.append(result_array)
            return result_array

        amount_zeros = int(ac.value[0])
        for i in range(0, amount_zeros):
            zig_zag.put_in_zig_zag(result_array, 0)

        length_of_koef = int(ac.value[1])
        if length_of_koef == 0:
            raise LengthToReadZeroException
        ac_koef = ac_haff_tree.get_next_n_bits(code, arr_for_index, length_of_koef)
        if ac_koef[0] != "1":
            ac_koef = int(ac_koef, 2) - 2 ** length_of_koef + 1
        else:
            ac_koef = int(ac_koef, 2)
        zig_zag.put_in_zig_zag(result_array, ac_koef)
        ac = ac_haff_tree.get_next_value(code, arr_for_index)


def quantization(image_info: ImageInfo):
    if len(image_info.quantization_tables) != 2:
        return

    for comp in image_info.components:
        quantization_table_id = comp.quantization_table_id
        quantization_table = image_info.get_quantization_table_by_id(quantization_table_id)
        for i, block in enumerate(comp.array_of_blocks):
            comp.array_of_blocks[i] = multiply_2d_matrixes(block, quantization_table.table)



def i_dct(image_info: ImageInfo):
    for i in range(0, len(image_info.y_channels)):
        image_info.y_channels[i] = idct(image_info.y_channels[i])
    for i in range(0, len(image_info.cb_channels)):
        image_info.cb_channels[i] = idct(image_info.cb_channels[i])
    for i in range(0, len(image_info.cr_channels)):
        image_info.cr_channels[i] = idct(image_info.cr_channels[i])


def convert_ycbcr_to_rgb(y, cb, cr):
    res = create_zeros_list(len(y), len(y[0]))
    for i in range(0, len(y)):
        for j in range(0, len(y[0])):
            R = y[i][j] + 1.402 * cr[i / 2][j / 2] + 128
            if R > 255:
                R = 255
            if R < 0:
                R = 0
            G = y[i][j] - 0.34414 * cb[i / 2][j / 2] - 0.71414 * cr[i / 2][j / 2] + 128
            if G > 255:
                G = 255
            if G < 0:
                G = 0
            B = y[i][j] + 1.772 * cb[i / 2][j / 2] + 128
            if B > 255:
                B = 255
            if B < 0:
                B = 0
            res[i][j] = [R, G, B]
    return res


def y_cb_cr_to_rgb(image_info: ImageInfo):
    arrays = []
    for i in range(0, len(image_info.y_channels)):
        rgb = convert_ycbcr_to_rgb(image_info.y_channels[i], image_info.cb_channels[0], image_info.cr_channels[0])
        arrays.append(rgb)
    m_rows = 2
    m_cols = 2
    # for i in range(m_cols // 2):

    rows = []

    for i in range(0, m_cols):
        #filling one row of matrixes
        one_row = []
        for j in range(0, m_cols):
            first = arrays.pop(0)
            one_row.append(first)
        while len(one_row) > 1:
            first = one_row.pop(0)
            second = one_row.pop(0)
            first_second_conc = append_right(first, second)
            one_row.append(first_second_conc + one_row)

        rows.append(one_row[0])

    result_matrix = rows
    while len(result_matrix) > 1:
        first = result_matrix.pop(0)
        second = result_matrix.pop(0)
        first_second_conc = append_down(first, second)
        result_matrix.append(first_second_conc + result_matrix)

    result_matrix = np.asarray(result_matrix[0], dtype=int)
    return result_matrix


with open("favicon.jpg", "rb") as f:
    img = f.read()
    bytes_array = BytesArray(img)
    image_info = ImageInfo()    #   для результата

    parse_ffd8(bytes_array)
    parse_fffe(bytes_array, image_info)
    parse_ffdb(bytes_array, image_info)
    parse_ffc0(bytes_array, image_info)
    parse_ffc4(bytes_array, image_info)
    parse_ffda(bytes_array, image_info)
    quantization(image_info)
    i_dct(image_info)
    result_matrix = y_cb_cr_to_rgb(image_info)
    # result_matrix = result_matrix / 255
    imshow(result_matrix)
    plt.show()

# даюовить проверку что заполнили всю матрицу
