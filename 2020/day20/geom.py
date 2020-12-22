EXAMPLE_ARR = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 9]]


def flipRows(arr):
    """ left(r)   to left
        top       to bottom
        right(r)  to right
        bottom    to top
    >>> flipRows(EXAMPLE_ARR)
    [[7, 8, 9], [4, 5, 6], [1, 2, 3]]
    >>> flipRows(flipRows(EXAMPLE_ARR)) == EXAMPLE_ARR
    True
    """
    return arr[::-1]


def flipCols(arr):
    """ left      to right
        top(r)    to top
        right     to left
        bottom(r) to bottom
    >>> flipCols(EXAMPLE_ARR)
    [[3, 2, 1], [6, 5, 4], [9, 8, 7]]
    >>> flipCols(flipCols(EXAMPLE_ARR)) == EXAMPLE_ARR
    True
    """
    return [col[::-1] for col in arr]


def rotate90(arr):
    """ left(r)  to top
        top      to right
        right(r) to bottom
        bottom   to left
    >>> rotate90(EXAMPLE_ARR)
    [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    >>> rotate90(rotate90(rotate90(rotate90(EXAMPLE_ARR)))) == EXAMPLE_ARR
    True
    """
    return [list(z) for z in zip(*arr[::-1])]


def rotate180(arr):
    """ left(r)   to right
        top(r)    to bottom
        right(r)  to left
        bottom(r) to top
    >>> rotate180(EXAMPLE_ARR)
    [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
    """
    return rotate90(rotate90(arr))


def rotate270(arr):
    """ left      to bottom
        top(r)    to left
        right     to top
        bottom(r) to right
    >>> rotate270(EXAMPLE_ARR)
    [[3, 6, 9], [2, 5, 8], [1, 4, 7]]
    """
    return rotate90(rotate90(rotate90(arr)))
