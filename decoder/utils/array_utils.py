import numpy as np


def create_num_py_array_float(input_list: []):
    np_arr = []
    for i in input_list:
        np_array_inner = np.asarray(i, dtype=float)
        np_arr.append(np_array_inner)

    return np.asarray(np_arr, dtype=float)


def create_zeros_array(N, M):
    result = []
    for i in range(N):
        result.append([])
        for j in range(0, M):
            result[i].append(0)

    return create_num_py_array_float(result)


def create_zeros_list(N, M):
    result = []
    for i in range(N):
        result.append([])
        for j in range(0, M):
            result[i].append(0)

    return result
