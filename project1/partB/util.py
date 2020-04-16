from numpy import nditer, reshape


def minMaxNormalize(array):
    array = ((array - array.min())/(array.max() - array.min())).reshape(array.shape)
    return array
