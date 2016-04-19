import matplotlib.pyplot as plt

import fieldgen
import conf
from combine import *


combines = []
field = None


def init():
    global field, combines
    field = fieldgen.get_field()
    for comb_shaft in conf.combines_shafts:
        combines.append(Combine(conf.shafts[comb_shaft], field))


def main():
    init()

    plt.imshow(field, interpolation='none')
    # plt.ion()
    plt.show()


if __name__ == '__main__':
    main()
