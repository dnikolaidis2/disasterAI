from numpy import nditer, reshape


def minMaxNormalize(array):
    arrayMin = array.min()
    arrayMax = array.max()

    with nditer(array, op_flags=['readwrite']) as it:
        for x in it:
            x[...] = (x - arrayMin) / (arrayMax - arrayMin)

    return array