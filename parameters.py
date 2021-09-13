import numpy as np
import random

# Density grid
grid_size = 40
dens = np.zeros((grid_size,grid_size))

# Sources
# dens[int(grid_size/2),int(grid_size/2)] = 20
# dens[int(grid_size/2)+1,int(grid_size/2)] = 20
# dens[int(grid_size/2),int(grid_size/2)+1] = 20
# dens[int(grid_size/2)+1,int(grid_size/2)+1] = 20

# X-velocity grid
x_vel = np.zeros((grid_size,grid_size))

b = 0.5
for row in range(grid_size):
    b += (0.5/grid_size)
    for ele in range(grid_size):
        x_vel[row,ele] = b #random.uniform(-1,1) #b # 0.5 # random.uniform(-0.5,0.5)

# Y-velocity grid
y_vel = np.zeros((grid_size,grid_size))

k = 0
for row in range(grid_size):
    k += (0.5/grid_size)
    for ele in range(grid_size):
        y_vel[row,ele] = k #random.uniform(-1,1) # -k*0 #random.uniform(-0.5,0.5)
