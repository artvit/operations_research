import matplotlib.pyplot as plt

import fieldgen
import conf
from combine import *
from factory import Factory


field = None
factory = None
combines = []


def init():
    global field, combines, factory
    factory = Factory()
    field = fieldgen.get_field()
    for i in range(conf.combines_num):
        combines.append(Combine(conf.shafts[conf.combines_shafts[i]], field, i))


def main():
    init()
    money = []
    # plt.figure()
    # image = plt.imshow(field, interpolation='none')
    for day in range(conf.days):
        for i in range(conf.combines_max_speed):
            for combine in combines:
                if combine.moves < combine.speed:
                    combine.move()
                    if combine.in_shaft:
                        factory.handle(combine)
        # image.set_array(field)
        # plt.draw()
        # plt.pause(.00001)
        for combine in combines:
            combine.moves = 0
        factory.complete_salt = 0
        factory.day_ending()
        day_money = factory.money
        day_money -= conf.combiners_salary * conf.combines_num
        for combine in combines:
            day_money -= combine.day_expanses
            combine.day_expanses = 0
        money.append(factory.money)
        print('day: ' + str(day))
    plt.figure()
    plt.plot(money)
    plt.show()


if __name__ == '__main__':
    main()
