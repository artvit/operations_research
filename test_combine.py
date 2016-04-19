import matplotlib.pyplot as plt
import numpy as np

import conf
from combine import Combine
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
combine = Combine(conf.shafts[2], field, 0)
# print(combine.find_way_to_nearest([80]), sep='\n')

plt.ion()
for i in range(270):
    combine.move()
    plt.imshow(field, interpolation='none')
    plt.draw()
    plt.pause(0.001)

# plt.imshow(field, interpolation='none')
# plt.show()
