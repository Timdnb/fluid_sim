import numpy as np
import random

# Density grid
grid_size = 40
dens = np.zeros((grid_size,grid_size))
show_vel = True

# Constants
diff_const_dens = 0
diff_const_vel = 0.05

# X-velocity grid
x_vel = np.zeros((grid_size,grid_size))

for row in range(grid_size):
    for ele in range(grid_size):
        x_vel[row,ele] = 1 #random.randint(-1,1)*random.uniform(0.8,1)

# Y-velocity grid
y_vel = np.zeros((grid_size,grid_size))

for row in range(grid_size):
    for ele in range(grid_size):
        y_vel[row,ele] = 0 #random.randint(-1,1)*random.uniform(0.8,1)

# Obstacles grid
obst = np.full((grid_size, grid_size), False, dtype=bool)
