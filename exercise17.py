import numpy as np

data = [[1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 3, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1]]


def find_nearest_pair(data):

    N = len(data)

    distances = []

    for i in range(0, N, 1):

        my_list = []
        for j in range(0, N, 1):

            if data[i] == data[j]:
                my_list.append(np.inf)

            else:

                manhattan = 0

                for k in range(0, len(data[j]), 1):
                    manhattan += np.abs(data[i][k] - data[j][k])

                my_list.append(manhattan)

        distances.append(my_list)

    # print(np.array(distances))

    dist = np.array(distances, dtype=np.float)
    print(np.unravel_index(np.argmin(dist), dist.shape))


find_nearest_pair(data)
