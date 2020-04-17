from numpy import unique, argwhere, take


def minMaxNormalize(array):
    array = ((array - array.min())/(array.max() - array.min())).reshape(array.shape)
    return array


def uniqueCounts(array, select=None):
    unq = unique(array, return_counts=True)
    if select is not None:
        ind = argwhere(unq[0] > select)
        return take(unq[1], ind).reshape(ind.size)
    else:
        return unq[1]
