import matplotlib.pyplot as plt

import fieldgen


field = fieldgen.gen_field()
plt.ion()
plt.imshow(field, interpolation='none')
plt.draw()
plt.pause(1)
print(plt.isinteractive())
field = fieldgen.add_shafts(field)
plt.imshow(field, interpolation='none')
plt.draw()
plt.pause(1)
field = fieldgen.add_mask(field)
plt.imshow(field, interpolation='none')
plt.draw()

input()
