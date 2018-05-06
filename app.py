from skimage.io import imread, imshow
from skimage.color import rgb2ycbcr
import math
import numpy as np
from numpy import split as split_array

from dct import dct


def transform_to_ycc(img):
    return rgb2ycbcr(img)


def check_size(img):
    return
    rows = img.shape[0]
    coloms = img.shape[1]
    if rows % 8 != 0:
        needed_rows = 8 - (rows % 8)
        pass#NEED TO DO


def get_one_channel(img, channel_number):
    res = []
    for i in range(0, len(img)):
        res.append([])
        for j in range(0, len(img[i])):
            res[i].append(img[i][j][channel_number])
    return res


def handle_parts(channel_img):
    new_channel_img = channel_img - 128
    y = get_one_channel(new_channel_img, 0)
    cb = get_one_channel(new_channel_img, 1)
    cr = get_one_channel(new_channel_img, 2)
    freq_y = dct(y)
    freq_cb = dct(cb)
    freq_cr = dct(cr)
    return


def split_on_parts(img):
    check_size(img)
    N = 8
    M = 8
    #   get first 8 elements
    channel_number_x = math.ceil(img.shape[0])
    channel_number_y = math.ceil(img.shape[1])
    for num_ch_x in range(0, channel_number_x):
        for num_ch_y in range(0, channel_number_y):
            part_img = []
            for i in range(0, N):
                part_img.append([])
                for j in range(0, M):
                    part_img[i].append(img[i][j])

            handle_parts(np.asarray(part_img))


img_rgb = imread("cat.jpg")
img_ycc = transform_to_ycc(img_rgb)
split_on_parts(img_ycc)
