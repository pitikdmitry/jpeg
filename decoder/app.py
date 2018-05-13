import math

import numpy as np
from skimage.io import imshow
from matplotlib import pyplot as plt
import scipy.fftpack
import binascii

from decoder.bytes_array import BytesArray
from decoder.exceptions.exceptions import BadMarkerException, BadDecodeException, BadDimensionException, \
    BadChannelsAmountException, BadQuantizationValuesLength, BadComponentsAmountException, LengthToReadZeroException, \
    BadMatrixParametersException, FullZigZagException, CodedDataParserException
from decoder.utils.component import Component
from decoder.utils.image_info import ImageInfo
from decoder.utils.array_utils import create_zeros_list, append_right, append_right, multiply_2d_matrixes, append_down
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
    if bytes_array[ff_ee_start] + bytes_array[ff_ee_start + 1] != 'fffe' \
            or bytes_array[ff_ee_start] + bytes_array[ff_ee_start + 1] != 'ffe0':
        # raise BadMarkerException
        pass

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
    max_horizontal_thinning = 0
    max_vertical_thinning = 0
    for i in range(0, channels_amount):
        channel_data = ff_c0_data[channel_info_index: channel_info_index + channel_data_size]
        component_id = int(channel_data[0], 16)
        horizontal_thinning = int(channel_data[1][0], 16)
        vertical_thinning = int(channel_data[1][1], 16)
        if component_id == 1:
            max_horizontal_thinning = horizontal_thinning
            max_vertical_thinning = vertical_thinning
        horizontal_thinning = max_horizontal_thinning // horizontal_thinning
        vertical_thinning = max_vertical_thinning // vertical_thinning
        quantization_table_id = int(channel_data[2], 16)
        image_info.add_component(Component(component_id, horizontal_thinning, vertical_thinning, quantization_table_id, image_info.width, image_info.height))

        channel_info_index += 3
    return


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

        image_info.haffman_trees.append(haff_tree)


def int_to_binstr(number, size):
    return bin(number)[2:][-size:].zfill(size)


def read_next_bytes(coded_data_16: str) -> []:
    coded_data_binary = ""
    previous_ch = ""
    for ch in coded_data_16:

        if ch == '00' and previous_ch == "ff":
            continue

        coded_data_binary += int_to_binstr(int(ch, 16), 8)
        previous_ch = ch

    return coded_data_binary


def parse_ffda(bytes_array: BytesArray, image_info: ImageInfo): # start of scan
    ffda_data = bytes_array.read_from_one_pair_to_other("ffda", "ffd9")
    header_length = int(ffda_data[2] + ffda_data[3], 16)   #   в первых ьдвух байтах длина только для заголовочной части а не для всей секции

    ffda_header_data = ffda_data[SECTION_TITLE_SIZE: header_length]
    ffda_header_index = 0
    amount_of_components = int(ffda_header_data[ffda_header_index + 2], 16)
    if amount_of_components != 3:
        raise BadComponentsAmountException

    # берем данные и переводим в двоичную строку(0111010...)
    coded_data = ffda_data[(header_length + 2):]
    coded_data_binary = read_next_bytes(coded_data)

    components_index = ffda_header_index + 3

    for i in range(0, amount_of_components):

        component_id = int(ffda_header_data[components_index], 16)
        dc_table_id = int(ffda_header_data[components_index + 1][1])
        ac_table_id = int(ffda_header_data[components_index + 1][0])

        component = image_info.get_component_by_id(component_id)
        component.dc_haff_table_id = dc_table_id
        component.ac_haff_table_id = ac_table_id

        components_index += 2

    parse_channels(image_info, coded_data_binary)


def parse_channels(image_info: ImageInfo, coded_data_binary: str):
    y_comp_index = 1
    cb_comp_index = 2
    cr_comp_index = 3

    y_component = image_info.get_component_by_id(y_comp_index)
    cb_component = image_info.get_component_by_id(cb_comp_index)
    cr_component = image_info.get_component_by_id(cr_comp_index)

    arr_for_index = [0]
    koef_cb = int(y_component.blocks_amount / cb_component.blocks_amount)
    koef_cr = int(y_component.blocks_amount / cr_component.blocks_amount)
    if koef_cb != koef_cr:
        raise BadComponentsAmountException
    y_amount = 0

    while y_amount < y_component.blocks_amount:
        for i in range(0, koef_cb):
            parse_channel(coded_data_binary, y_component, image_info, arr_for_index)
            y_amount += 1

        parse_channel(coded_data_binary, cb_component, image_info, arr_for_index)
        parse_channel(coded_data_binary, cr_component, image_info, arr_for_index)

    length_of_data = len(coded_data_binary)
    length_index = arr_for_index[0]
    if arr_for_index[0] != len(coded_data_binary) - 1: # 136 for favicon
        # raise CodedDataParserException
        print("length_of_data: " + str(length_of_data) + " length_index: " + str(length_index))
        pass

    for comp in image_info.components:
        comp.substract_dc()


def parse_channel(code: str, component: Component, image_info: ImageInfo, arr_for_index: []):
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
    if dc.value != "00":
        length_to_read = int(dc.value, 16)  #   changed to 16
        if length_to_read == 0:
            raise LengthToReadZeroException

        dc_koef = dc_haff_tree.get_next_n_bits(code, arr_for_index, length_to_read)
        if dc_koef[0] != "1":
            dc_koef = int(dc_koef, 2) - 2 ** length_to_read + 1
        else:
            dc_koef = int(dc_koef, 2)
    zig_zag.put_in_zig_zag(dc_koef)

    #   reading ac
    ac = ac_haff_tree.get_next_value(code, arr_for_index)
    while True:
        if ac.value == "root" or ac.value == "node":
            raise BadDecodeException
        if ac.value == "00":
            component.array_of_blocks.append(zig_zag.data)
            return

        amount_zeros = int(ac.value[0], 16)    #   added 16
        for i in range(0, amount_zeros):
            answer = zig_zag.put_in_zig_zag(0)
            if answer == -1:
                raise FullZigZagException

        length_of_koef = int(ac.value[1], 16)   #   added 16
        if length_of_koef == 0:
            raise LengthToReadZeroException
        ac_koef = ac_haff_tree.get_next_n_bits(code, arr_for_index, length_of_koef)
        if ac_koef[0] != "1":
            ac_koef = int(ac_koef, 2) - 2 ** length_of_koef + 1
        else:
            ac_koef = int(ac_koef, 2)
        answer = zig_zag.put_in_zig_zag(ac_koef)
        if answer == -1:
            raise FullZigZagException

        if zig_zag.check_size() <= 0:
            component.array_of_blocks.append(zig_zag.data)
            return
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
    for comp in image_info.components:
        for i, block in enumerate(comp.array_of_blocks):
            comp.array_of_blocks[i] = idct(block)
    return


def convert_ycbcr_to_rgb(y, cb, cr, part_number, K):
    h_offset = 0
    v_offset = 0
    if part_number == 1:
        h_offset = N // 2
    elif part_number == 2:
        v_offset = M // 2
    if part_number == 3:
        v_offset = M // 2
        h_offset = N // 2

    res = create_zeros_list(N, M)
    for i in range(0, N):
        for j in range(0, M):
            R = y[i][j] + 1.402 * cr[i // 2 * K + v_offset][j // 2 * K + h_offset] + 128
            if R > 255:
                R = float(255)
            if R < 0:
                R = float(0)
            G = y[i][j] - 0.34414 * cb[i // 2 * K + v_offset][j // 2 * K + h_offset] \
                - 0.71414 * cr[i // 2 * K + v_offset][j // 2 * K + h_offset] + 128
            if G > 255:
                G = float(255)
            if G < 0:
                G = float(0)
            B = y[i][j] + 1.772 * cb[i // 2 * K + v_offset][j // 2 * K + h_offset] + 128
            if B > 255:
                B = float(255)
            if B < 0:
                B = float(0)
            res[i][j] = [R, G, B]
    return res


def merge_one_block(one_block_arr: []):
    if len(one_block_arr) != 4:
        return

    first = one_block_arr.pop(0)
    second = one_block_arr.pop(0)
    third = one_block_arr.pop(0)
    fourth = one_block_arr.pop(0)

    first_second_conc = append_right(first, second)
    third_fourth_conc = append_right(third, fourth)
    four_conc = append_down(first_second_conc, third_fourth_conc)
    return four_conc


def convert_by_blocks(y_component: Component, cb_component: Component, cr_component: Component, rgb_components_array: [], K: int):
    y_index = 0
    cb_index = 0
    cr_index = 0
    while y_index < y_component.blocks_amount:
        one_block_arr = []
        for part_number in range(0, 4):
            rgb_component = convert_ycbcr_to_rgb(y_component.array_of_blocks[y_index],
                                                 cb_component.array_of_blocks[cb_index],
                                                 cr_component.array_of_blocks[cr_index], part_number, K)
            one_block_arr.append(rgb_component)
            y_index += 1

        one_block = merge_one_block(one_block_arr)
        cb_index += 1
        cr_index += 1

        rgb_components_array.append(one_block)


def y_cb_cr_to_rgb(image_info: ImageInfo):
    y_comp_index = 1
    cb_comp_index = 2
    cr_comp_index = 3

    y_component = image_info.get_component_by_id(y_comp_index)
    cb_component = image_info.get_component_by_id(cb_comp_index)
    cr_component = image_info.get_component_by_id(cr_comp_index)

    rgb_components_array = []
    koef_cb = int(y_component.blocks_amount / cb_component.blocks_amount)
    if koef_cb == 4:
        convert_by_blocks(y_component, cb_component, cr_component, rgb_components_array, 1)
    elif koef_cb == 1:
        for i in range(0, y_component.blocks_amount):
            convert_ycbcr_to_rgb(y_component.array_of_blocks[i], cb_component.array_of_blocks[i],
                                 cr_component.array_of_blocks[i], 0, 2)
    else:
        raise BadComponentsAmountException
    return rgb_components_array


def merge_rgb_blocks(rgb_components_array: [], image_info: ImageInfo):
    if image_info.width % M != 0 or image_info.height % N != 0:
        raise BadMatrixParametersException

    m_cols = math.floor(math.sqrt(len(rgb_components_array)))
    m_rows = m_cols

    # blocks_from_squares = []
    # for i in range(0, len(rgb_components_array) // 4):
    #     first = rgb_components_array.pop(0)
    #     second = rgb_components_array.pop(0)
    #     third = rgb_components_array.pop(0)
    #     fourth = rgb_components_array.pop(0)
    #
    #     first_second_conc = append_right(first, second)
    #     third_fourth_conc = append_right(third, fourth)
    #     four_conc = append_down(first_second_conc, third_fourth_conc)
    #
    #     blocks_from_squares.append(four_conc)
    #     # f = np.asarray(four_conc, dtype=int)
    #     # imshow(f)
    #     # plt.show()
    #
    # m_rows = len(blocks_from_squares) // (N // 4)
    # m_cols = len(blocks_from_squares) // (M // 4)
    # rgb_components_array = blocks_from_squares


    # for i in range(0, len(rgb_components_array)):
    #     for j in range(0, len(rgb_components_array[i])):
    #         for k in range(0, len(rgb_components_array[i][j])):
    #             print(int(rgb_components_array[i][j][k][0]), end=" ")
    #         print("")
    #     print("")
    #     print("")
    #     print("")

    rows = []
    for i in range(0, m_rows):
        #filling one row of matrixes
        one_row = []
        for j in range(0, m_cols):
            first = rgb_components_array.pop(0)
            one_row.append(first)
        while len(one_row) > 1:
            first = one_row.pop(0)
            second = one_row.pop(0)
            first_second_conc = append_right(first, second)
            # f = np.asarray(first_second_conc, dtype=int)
            # imshow(f)
            # plt.show()


            new_arr = []
            new_arr.append(first_second_conc)
            for mass in one_row:
                new_arr.append(mass)

            one_row = new_arr

        rows.append(one_row[0])

    result_matrix = rows
    while len(result_matrix) > 1:
        first = result_matrix.pop(0)
        second = result_matrix.pop(0)
        first_second_conc = append_down(first, second)

        new_arr = []
        new_arr.append(first_second_conc)
        for mass in result_matrix:
            new_arr.append(mass)
        result_matrix = new_arr

    result_matrix = np.asarray(result_matrix[0], dtype=int)
    return result_matrix


def print_array(arr):
    pass
    # for i in range(0, len(arr)):
    #     for j in range(0, len(arr[i])):
    #         print(int(arr[i][j][0]), end=" ")
    #     print("")
    # print("")
    # print("")


with open("skype.jpg", "rb") as f:
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
    rgb_components_array = y_cb_cr_to_rgb(image_info)
    result_matrix = merge_rgb_blocks(rgb_components_array, image_info)
    # result_matrix = result_matrix / 255
    imshow(result_matrix)
    plt.show()

# даюовить проверку что заполнили всю матрицу
