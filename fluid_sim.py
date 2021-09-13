import numpy as np
import pygame as pg
import time

# Other files
from parameters import grid_size, dens,x_vel, y_vel
from fluid_draw import draw

# Links
# http://graphics.cs.cmu.edu/nsp/course/15-464/Fall09/papers/StamFluidforGames.pdf
# https://www.youtube.com/watch?v=qsYE1wMEMPA

def diffuse(a, arr):
    """
    Function to update every array cell based on its average surroundings for a certain property
    """
    # Add padding in 4 different ways
    arr1 = np.pad(arr, ((2,0),(1,1)), constant_values=0)
    arr2 = np.pad(arr, ((0,2),(1,1)), constant_values=0)
    arr3 = np.pad(arr, ((1,1),(2,0)), constant_values=0)
    arr4 = np.pad(arr, ((1,1),(0,2)), constant_values=0)

    # Calculate average of each square based on the 4 neighbouring squares
    avg_arr = a * (arr1 + arr2 + arr3 + arr4) / 4

    # Add sides to row besides it
    avg_arr[1] += avg_arr[0]
    avg_arr[grid_size] += avg_arr[grid_size+1]
    avg_arr[:,1] += avg_arr[:,0]
    avg_arr[:,grid_size] += avg_arr[:,grid_size+1]

    # Now remove the padding that was initially added
    avg_arr = avg_arr[1:-1, 1:-1]

    # Calculate the new values based on the current values and the average neighbouring values
    arr = (1-a)*arr + avg_arr

    return arr

def simulate(dens, x_vel, y_vel):
    """
    Simulate the whole fluid
    """
    running = True

    while running:
        # time.sleep(1)
        # ------------------------------ Diffusion of density ------------------------------
        dens = diffuse(0.1, dens)

        # ------------------------------ Diffusion of velocities ------------------------------
        x_vel = diffuse(0.005, x_vel)
        y_vel = diffuse(0.005, y_vel)

        # ------------------------------ Advection of velocities ------------------------------
        # X-velocity
        # Separate positive and negative x-velocities
        x_vel_pos = np.where(x_vel>0, x_vel, 0)
        x_vel_neg = np.where(x_vel<0, x_vel, 0)

        # Calculate density that will be moved away
        x_vel_pos_dens = x_vel_pos*dens
        x_vel_neg_dens = x_vel_neg*dens

        # Subtract this density from the squares where it is at
        dens -= (x_vel_pos_dens + abs(x_vel_neg_dens))

        # Move positive densities to the right and negative to the left
        dens_x_vel1 = np.pad(x_vel_pos_dens, ((0,0),(2,0)), constant_values=0)
        dens_x_vel2 = np.pad(x_vel_neg_dens, ((0,0),(0,2)), constant_values=0)

        # Now add the densities to the squares where it moved to
        x_vel_add_dens = dens_x_vel1 + abs(dens_x_vel2)
        x_vel_add_dens[:,1] += x_vel_add_dens[:,0]
        x_vel_add_dens[:,-2] += x_vel_add_dens[:,-1]
        x_vel_add_dens = x_vel_add_dens[0:grid_size, 1:-1]

        dens += x_vel_add_dens

        # Y-velocity
        # Separate positive and negative y-velocities
        y_vel_pos = np.where(y_vel>0, y_vel, 0)
        y_vel_neg = np.where(y_vel<0, y_vel, 0)

        # Calculate density that will be moved away
        y_vel_pos_dens = y_vel_pos*dens
        y_vel_neg_dens = y_vel_neg*dens

        # Subtract this density from the squares where it is at
        dens -= (y_vel_pos_dens + abs(y_vel_neg_dens))

        # Move positive densities up and negative down
        dens_y_vel1 = np.pad(y_vel_pos_dens, ((0,2),(0,0)), constant_values=0)
        dens_y_vel2 = np.pad(y_vel_neg_dens, ((2,0),(0,0)), constant_values=0)

        # Now add the densities to the squares where it moved to
        y_vel_add_dens = dens_y_vel1 + abs(dens_y_vel2)
        y_vel_add_dens[1,:] += y_vel_add_dens[0,:]
        y_vel_add_dens[-2,:] += y_vel_add_dens[-1,:]
        y_vel_add_dens = y_vel_add_dens[1:-1, 0:grid_size]

        dens += y_vel_add_dens

        # Draw the density (higher density = darker)
        draw(dens, x_vel, y_vel)

        # Press "C" to clean entire board
        pg.event.pump()
        keys = pg.key.get_pressed()

        if keys[pg.K_c]:
            dens = np.zeros((grid_size,grid_size))

# Run
simulate(dens, x_vel, y_vel)




