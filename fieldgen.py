import numpy as np

import conf


mask_const = conf.mask_const
shaft_const = conf.shaft_const
mask = [3, 1, 2, 0]


def gen_field(m=100):
    assert not m % 2
    field = np.empty(shape=(m, m), dtype=np.int8)
    for k in range(m // 2):
        if k % 2:
            for i in range(2 * (k + 1)):
                field[m / 2 - 1 - k][m / 2 - 1 - k + i] = 80 if i % 2 else 50
                field[m / 2 + k][m / 2 - 1 - k + i] = 50 if i % 2 else 80
            for i in range(2 * k):
                field[m / 2 - 1 - k + i + 1][m / 2 - 1 - k] = 50 if i % 2 else 80
                field[m / 2 - 1 - k + i + 1][m / 2 + k] = 80 if i % 2 else 50
        else:
            for i in range(2 * (k + 1)):
                field[m / 2 - 1 - k][m / 2 - 1 - k + i] = 20
                field[m / 2 + k][m / 2 - 1 - k + i] = 20
            for i in range(2 * k):
                field[m / 2 - 1 - k + i + 1][m / 2 - 1 - k] = 20
                field[m / 2 - 1 - k + i + 1][m / 2 + k] = 20
    return field


def add_mask(field: np.ndarray):
    t_field = None
    for k in range(4):
        good = True
        t_field = field.copy()
        for i in range(field.shape[0]):
            for j in range(mask[(i + k) % 4], field.shape[1], 4):
                if t_field[i, j] != shaft_const:
                    t_field[i, j] = mask_const
                else:
                    good = False
        else:
            if good:
                break
    return t_field


def add_shafts(field: np.ndarray):
    t_field = field.copy()
    for shaft in conf.shafts:
        t_field[shaft[1], shaft[0]] = shaft_const
    return t_field


def get_field():
    field = gen_field()
    field = add_shafts(field)
    field = add_mask(field)
    return field
