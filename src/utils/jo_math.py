import math


def round_down(x, a):
    return math.floor(x / a) * a


def round_nearest(x, a):
    return round(x / a) * a
