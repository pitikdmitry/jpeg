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


def get_array_from_list(l: []):
    result = np.asarray(l, dtype=float)
    return result


def multiply_matrix(matrix1, matrix2):
    res = create_zeros_list(len(matrix1[0]), len(matrix1[1]))
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                # resulted matrix
                res[i][j] += matrix1[i][k] * matrix2[k][j]
    return res
