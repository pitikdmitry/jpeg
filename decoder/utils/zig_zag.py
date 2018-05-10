from decoder.utils.array_utils import create_zeros_array, create_zeros_list


class ZigZag:
    def __init__(self):
        self._up = True
        self._i = 0
        self._j = 0
        self._counter = 0

    def zig_zag_order(self, arr):
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

    def put_in_zig_zag(self, result, element):
        N, M = 8, 8

        if self._i == 0 and self._j == 0:
            result[self._i][self._j] = element
            self._counter += 1
            return

        while self._counter < N * M - 1:
            if not self._up:  #   down
                while 0 <= self._i < N - 1 and 0 < self._j < M:
                    self._j -= 1
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                if 0 < self._i < N - 1:
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                elif 0 <= self._j< M - 1:
                    self._j += 1
                    result[i][j] = element
                    self._counter += 1
                    return
                self._up = True
            else:   #   up
                while 0 < self._i < N and 0 <= self._j < M - 1:
                    self._j += 1
                    self._i -= 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                if 0 <= self._j< M - 1:
                    self._j += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                elif 0 <= self._i < N - 1:
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                self._up = False

        return
