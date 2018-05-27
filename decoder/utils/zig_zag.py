from decoder.utils.array_utils import create_zeros_list


class ZigZag:
    def __init__(self):
        self._up = True
        self._i = 0
        self._j = 0
        self._counter = 0
        self._N = 8
        self._M = 8
        self._arr = create_zeros_list(self._N, self._M)
        self._max_size = self._M * self._N

        self._usual_array = []

    @property
    def size(self) -> int:
        return self._counter

    @property
    def max_size(self) -> int:
        return self._max_size

    @property
    def data(self) -> []:
        return self._arr

    def check_size(self, amount_to_add: int = 0) -> int:
        return self.max_size - (self._counter + amount_to_add)

    def zig_zag_order(self, arr):
        N, M = self._N, self._M
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

    def put_in_zig_zag(self, element):
        self._usual_array.append(element)
        N, M = self._N, self._M
        if self._counter + 1 > self._max_size:
            return -1

        if self._counter == 0:
            self._arr[self._i][self._j] = element
            self._counter += 1
            return

        if self._counter < N * M:
            if not self._up:  #   down
                if 0 <= self._i < N - 1 and 0 < self._j < M:
                    self._j -= 1
                    self._i += 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1
                    return
                else:
                    self._up = True

                if 0 < self._i < N - 1:
                    self._i += 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1
                elif 0 <= self._j < M - 1:
                    self._j += 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1
            else:   #   up
                if 0 < self._i < N and 0 <= self._j < M - 1:
                    self._j += 1
                    self._i -= 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1
                    return
                else:
                    self._up = False

                if 0 <= self._j < M - 1:
                    self._j += 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1
                elif 0 <= self._i < N - 1:
                    self._i += 1
                    self._arr[self._i][self._j] = element
                    self._counter += 1

        return self._counter


if __name__ == "__main__":
    zig = ZigZag()
    res_arr = create_zeros_list(8, 8)
    for i in range(0, 64):
        if i == 63:
            print(63)
        zig.put_in_zig_zag(res_arr, i)
    # print(res_arr)