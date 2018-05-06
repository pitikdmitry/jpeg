from numpy import split as split_array
import numpy as np


N = 24
img = np.random.rand(N)
splitted_array = split_array(img, N / 8)
pass