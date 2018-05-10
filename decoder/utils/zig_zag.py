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
        while counter < N * M:
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

        if self._counter == 0:
            result[self._i][self._j] = element
            self._counter += 1
            return

        if self._counter < N * M:
            if not self._up:  #   down
                if 0 <= self._i < N - 1 and 0 < self._j < M:
                    self._j -= 1
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                else:
                    self._up = True

                if 0 < self._i < N - 1:
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                elif 0 <= self._j < M - 1:
                    self._j += 1
                    result[self._i][self._j] = element
                    self._counter += 1
            else:   #   up
                if 0 < self._i < N and 0 <= self._j < M - 1:
                    self._j += 1
                    self._i -= 1
                    result[self._i][self._j] = element
                    self._counter += 1
                    return
                else:
                    self._up = False

                if 0 <= self._j < M - 1:
                    self._j += 1
                    result[self._i][self._j] = element
                    self._counter += 1
                elif 0 <= self._i < N - 1:
                    self._i += 1
                    result[self._i][self._j] = element
                    self._counter += 1

        return

if __name__ == "__main__":
    zig = ZigZag()
    res_arr = create_zeros_list(8, 8)
    for i in range(0, 64):
        if i == 63:
            print(63)
        zig.put_in_zig_zag(res_arr, i)
    # print(res_arr)