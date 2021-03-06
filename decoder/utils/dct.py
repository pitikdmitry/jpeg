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


def idct(fx):
    fx = np.asarray(fx, dtype=float)
    N = fx.shape[0]
    M = fx.shape[1]

    result = create_result(N, M)
    for m in range(0, M):
        for n in range(0, N):

            z = 0 # для резулятата
            for k in range(0, N):
                for l in range(0, M):
                    cos_m_k = cos(((2 * m + 1) * k * pi) / (2 * M))
                    cos_n_l = cos(((2 * n + 1) * l * pi) / (2 * N))
                    X_k_l = fx[k][l]

                    c_k, c_l = 1, 1
                    if k == 0:
                        c_k = 1 / sqrt(2)
                    if l == 0:
                        c_l = 1 / sqrt(2)
                    z += c_k * c_l * X_k_l * cos_m_k * cos_n_l

            z = (2 * z) / sqrt(M * N)

            result[m][n] = z

    return result


if __name__ == "__main__":
    input_arr = np.asarray([[52,55,61,66,70,61,64,73],
                 [63,59,55,90,109,85,69,72],
                 [62,59,68,113,144,104,66,73],
                 [63,58,71,122,154,106,70,69],
                 [67,61,68,104,126,88,68,70],
                 [79,65,60,70,77,68,58,75],
                 [85,71,64,59,55,61,65,83],
                 [87,79,69,68,65,76,78,94]])
    input_arr -= 128
    freq = dct(input_arr)
    pass

