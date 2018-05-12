import numpy as np

from decoder.exceptions.exceptions import ConcatenateException, BadMatrixesMultiplyException


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


# def multiply_matrix(matrix1, matrix2):
#     res = create_zeros_list(len(matrix1[0]), len(matrix1[1]))
#     for i in range(len(matrix1)):
#         for j in range(len(matrix2[0])):
#             for k in range(len(matrix2)):
#                 # resulted matrix
#                 res[i][j] += matrix1[i][k] * matrix2[k][j]
#     return res


def append_right(matrix1, matrix2):
    m_1_rows = len(matrix1)
    m_2_rows = len(matrix2)

    if m_1_rows != m_2_rows:
        raise ConcatenateException

    for i in range(0, m_1_rows):
        matrix1.append(matrix2[i])

    return matrix1


def append_down(matrix1, matrix2):
    m_1_rows = len(matrix1)
    m_2_rows = len(matrix2)

    if m_1_rows != m_2_rows:
        raise ConcatenateException

    for i in range(0, m_1_rows):
        for j in range(0, len(matrix2[i])):
            matrix1[i].append(matrix2[i][j])

    return matrix1


def multiply_2d_matrixes(matrix1: [], matrix2: []):
    res = create_zeros_list(len(matrix1), len(matrix1[0]))

    if len(matrix1) != len(matrix2):
        raise BadMatrixesMultiplyException
    for i in range(0, len(matrix1)):
        if len(matrix1[i]) != len(matrix2[i]):
            raise BadMatrixesMultiplyException
        for j in range(0, len(matrix1[i])):
            res[i][j] = matrix1[i][j] * matrix2[i][j]
