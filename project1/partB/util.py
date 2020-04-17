from numpy import unique, argwhere, take


def minMaxNormalize(array, min=None, max=None):
    if min is None:
        min = array.min()

    if max is None:
        max = array.max()

    return ((array - min)/(max - min)).reshape(array.shape)


def uniqueCounts(array, select=None):
    unq = unique(array, return_counts=True)
    if select is not None:
        ind = argwhere(unq[0] > select)
        return take(unq[1], ind).reshape(ind.size)
    else:
        return unq[1]
