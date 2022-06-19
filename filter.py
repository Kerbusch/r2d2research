from copy import deepcopy

import numpy as np


# Median filter with 3 tabs
def medianFilter(data):
    data_copy = deepcopy(data)
    for i in range(2, len(data) - 2):
        for j in range(len(data[i])-1):
            data_copy[i][j] = np.median(
                (data_copy[i - 2][j], data_copy[i - 1][j], data_copy[i][j], data_copy[i + 1][j], data_copy[i + 2][j]))

    return data_copy


# Average filter with n tabs
def averageFilter(data, tabs):
    # needs to be uneven otherwise it will add 1 to the tabs
    if tabs % 2 == 0:
        tabs += 1
    data_copy = deepcopy(np.array(data))

    tabs_list = [1/tabs] * tabs

    for i in range(6):
        data_copy[tabs//2:-(tabs//2), i] = np.convolve(data_copy[:, i], tabs_list, 'valid')

    return data_copy
        