from decoder.utils.array_utils import create_zeros_array, create_zeros_list


def zig_zag_order(arr):
    N, M = 8, 8
    i, j, counter = 0, 0, 0
    result = create_zeros_list(N, M)
    result[i][j] = arr[counter]
    counter += 1

    up = True
    while counter < N * M - 1:
        if not up:  #   down
            while 0 <= i < N - 1 and 0 < j < M:
                j -= 1
                i += 1
                result[i][j] = arr[counter]
                counter += 1
            if 0 < i < N - 1:
                i += 1
                result[i][j] = arr[counter]
                counter += 1
            elif 0 <= j < M - 1:
                j += 1
                result[i][j] = arr[counter]
                counter += 1
            up = True
        else:   #   up
            while 0 < i < N and 0 <= j < M - 1:
                j += 1
                i -= 1
                result[i][j] = arr[counter]
                counter += 1
            if 0 <= j < M - 1:
                j += 1
                result[i][j] = arr[counter]
                counter += 1
            elif 0 <= i < N - 1:
                i += 1
                result[i][j] = arr[counter]
                counter += 1
            up = False

    return result


