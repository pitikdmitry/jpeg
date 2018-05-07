import numpy as np
from numpy import cos, pi, sqrt


def create_num_py_array(input_list: []):
    np_arr = []
    for i in input_list:
        np_array_inner = np.asarray(i, dtype=float)
        np_arr.append(np_array_inner)

    return np.asarray(np_arr, dtype=float)


def create_result(N, M):
    result = []
    for i in range(N):
        result.append([])
        for j in range(0, M):
            result[i].append(0)

    result = create_num_py_array(result)
    return result


def dct(fx):
    fx = np.asarray(fx, dtype=float)
    N = fx.shape[0]
    M = fx.shape[1]

    result = create_result(N, M)
    for k in range(0, N):
        for l in range(0, M):

            z = 0 # для резулятата
            for n in range(0, N):
                for m in range(0, M):
                    cos_m_k = cos(((2 * m + 1) * k * pi) / 2 * M)
                    cos_n_l = cos(((2 * n + 1) * l * pi) / 2 * N)
                    x_m_n = fx[n][m]   # действительная часть значения яркости пикселя
                    z += x_m_n * cos_m_k * cos_n_l

            c_k, c_l = 1, 1
            if k == 0:
                c_k = 1 / sqrt(2)
            if l == 0:
                c_l = 1 / sqrt(2)
            z = z * c_k * c_l

            result[k][l] = z

    return result
