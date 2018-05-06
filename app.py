from skimage.io import imread, imshow
from skimage.color import rgb2ycbcr
from numpy import split as split_array


def transform_to_ycc(img):
    return rgb2ycbcr(img)


def split_on_channels(img):
    for line in img:
        splitted_line =












img_rgb = imread("parrots.jpeg")
img_ycc = transform_to_ycc(img_rgb)
