import numpy as np
x = [8,7,6,5,4]
x = np.array(x)
y = x[1:3]
print(x)
print(y)
y[0] = 2
print(x)
print(y)