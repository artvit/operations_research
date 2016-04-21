import matplotlib.pyplot as plt
import numpy as np

import conf
from combine import Combine
from factory import Factory
import fieldgen


field = fieldgen.get_field()

# plt.ion()
combines = []
for i in range(conf.combines_num):
    combines.append(Combine(conf.shafts[conf.combines_shafts[i]], field, i))

factory = Factory()

money = []

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
        # plt.pause(.001)
    for combine in combines:
        combine.moves = 0
    factory.complete_salt = 0
    factory.day_ending()

    money.append(factory.money)
    print('day: ' + str(day))
plt.plot(money)
plt.show()

