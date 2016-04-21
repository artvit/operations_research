import matplotlib.pyplot as plt

import fieldgen
import conf
from combine import *


combines = []
field = None


def init():
    global field, combines
    field = fieldgen.get_field()
    for i in range(conf.combines_num):
        combines.append(Combine(conf.shafts[conf.combines_shafts[i]], field, i))


def main():
    init()
    for _ in range(conf.days):
        for i in range(conf.combines_max_speed):
            for combine in combines:
                if combine.moves < combine.speed:
                    combine.move()
        for combine in combines:
            combine.moves = 0
    # plt.imshow(field, interpolation='none')
    # plt.ion()
    # plt.show()


if __name__ == '__main__':
    main()
