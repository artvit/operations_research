import matplotlib.pyplot as plt
import numpy as np

import conf
from combine import Combine
from factory import Factory
import fieldgen


# field = fieldgen.gen_field(10)
sh = conf.shaft_const
# field = [
#     [20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
#     [20, 50, 80, 50, 80, 50, 80, 50, 80, 20],
#     [20, 80, 20, 20, 20, 20, 20, 20, 50, 20],
#     [20, 50, 20, 50, 80, 50, 80, 20, 80, 20],
#     [20, 80, 20, 80,  0,  0, 50, 20, 50, 20],
#     [20, 50, 20, 50, sh,  0, 80, 20, 80, 20],
#     [20, 80, 20, 80,  0, 80, 50, 20, 50, 20],
#     [20, 50, 20, 20, 20, 20, 20, 20, 80, 20],
#     [20, 80, 50, 80, 50, 80, 50, 80, 50, 20],
#     [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
# ]
# field = np.array(field, dtype=np.int8)
# field = fieldgen.add_mask(field)
field = fieldgen.get_field()

# plt.ion()
combines = []
for i in range(conf.combines_num):
    combines.append(Combine(conf.shafts[conf.combines_shafts[i]], field, i))

factory = Factory()

for _ in range(conf.days):
    for i in range(conf.combines_max_speed):
        for combine in combines:
            if combine.moves < combine.speed:
                combine.move()
                if combine.in_shaft:
                    factory.handle(combine)
        plt.imshow(field, interpolation='none')
        plt.draw()
        plt.pause(0.001)
    for combine in combines:
        combine.moves = 0

# combine = Combine(conf.shafts[2], field, 0)
# combine2 = Combine(conf.shafts[2], field, 1)
# combine3 = Combine(conf.shafts[1], field, 2)
# print(combine.find_way_to_nearest([80]), sep='\n')
# for i in range(270):
#     combine.move()
#     combine2.move()
#     combine3.move()
#     plt.imshow(field, interpolation='none')
#     plt.draw()
#     plt.pause(0.001)

# plt.ioff()
# plt.imshow(field, interpolation='none')
# plt.show()
