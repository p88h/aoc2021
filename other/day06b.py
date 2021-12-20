import numpy as np
t = np.array([[0,1,0,0,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,1,0,0],
              [1,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,1],
              [1,0,0,0,0,0,0,0,0]])
v = np.bincount(list(map(int, input().split(","))), minlength=9)
print(np.dot(np.linalg.matrix_power(t, 256), v).sum())