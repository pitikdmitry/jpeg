import numpy as np
from skimage.io import imshow, imread
from matplotlib import pyplot as plt


arr = imread("5.jpg")
arr = np.asarray(arr, dtype=int)
imshow(arr)
plt.show()