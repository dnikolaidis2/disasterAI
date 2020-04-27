from numpy import unique, argwhere, take, zeros, put, all


def minMaxNormalize(array, min=None, max=None):
    if min is None:
        min = array.min()

    if max is None:
        max = array.max()

    return ((array - min)/(max - min)).reshape(array.shape)


def uniqueCounts(array, select=None, expected_elems=None):
    unq = unique(array, return_counts=True)
    if select is not None:
        ind = argwhere(unq[0] > select)
        if all(take(unq[0], ind).reshape(ind.size) == expected_elems):
            return take(unq[1], ind).reshape(ind.size)

        ret = zeros(expected_elems.shape, dtype=int)
        if take(unq[0], ind).size == 0:
            return ret

        # TODO make this actually problem agnostic maybe(At this point who even cares)
        put(ret, (take(unq[0], ind).reshape(ind.size) - 1).astype(int), take(unq[1], ind).reshape(ind.size))
        return ret
    else:
        return unq[1]
