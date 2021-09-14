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

        # ------------------------------ Diffusion of velocities ---------------------------
        x_vel = diffuse(0.05, x_vel)
        y_vel = diffuse(0.05, y_vel)

        # ------------------------------ Advection -----------------------------------------
        # X-velocity
        # Separate positive and negative x-velocities
        x_vel_pos = np.where(x_vel>0, x_vel, 0)
        x_vel_neg = np.where(x_vel<0, x_vel, 0)

        # Calculate density that will be moved away, used the logistic function to prevent overflow because of velocities > 1 (should be fixed in future)
        x_vel_pos_dens = -(1/(1+np.exp(x_vel_pos))-0.5)*dens
        x_vel_neg_dens = -(1/(1+np.exp(x_vel_neg))-0.5)*dens

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

        # Calculate density that will be moved away, used the logistic function to prevent overflow because of velocities > 1 (should be fixed in future)
        y_vel_pos_dens = -(1/(1+np.exp(y_vel_pos))-0.5)*dens
        y_vel_neg_dens = -(1/(1+np.exp(y_vel_neg))-0.5)*dens

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

        # --------------------- Walls
        x_vel[:,0] = 0
        x_vel[:,-1] = 0
        y_vel[0,:] = 0
        y_vel[-1,:] = 0

        # ------------------------------ Self-Advection of velocities ----------------------
        # # X-velocity
        # # Separate positive and negative x-velocities
        # x_vel_pos = np.where(x_vel>0, x_vel, 0)
        # x_vel_neg = np.where(x_vel<0, x_vel, 0)

        # # Calculate velocity that will be moved away
        # x_vel_pos_tr = x_vel_pos*0.05
        # x_vel_neg_tr = x_vel_neg*0.05

        # # Subtract this velocity from the squares where it is at
        # x_vel -= (x_vel_pos_tr + abs(x_vel_neg_tr))

        # # Move positive velocities to the right and negative to the left
        # tr_x_vel1 = np.pad(x_vel_pos_tr, ((0,0),(2,0)), constant_values=0)
        # tr_x_vel2 = np.pad(x_vel_neg_tr, ((0,0),(0,2)), constant_values=0)

        # # Now add the velocities to the squares where it moved to
        # x_vel_add_vel = tr_x_vel1 + abs(tr_x_vel2)
        # x_vel_add_vel[:,1] += x_vel_add_vel[:,0]
        # x_vel_add_vel[:,-2] += x_vel_add_vel[:,-1]
        # x_vel_add_vel = x_vel_add_vel[0:grid_size, 1:-1]

        # x_vel += x_vel_add_vel

        # # Y-velocity
        # # Separate positive and negative y-velocities
        # y_vel_pos = np.where(y_vel>0, y_vel, 0)
        # y_vel_neg = np.where(y_vel<0, y_vel, 0)

        # # Calculate velocity that will be moved away
        # y_vel_pos_tr = y_vel_pos*0.05
        # y_vel_neg_tr = y_vel_neg*0.05

        # # Subtract this velocity from the squares where it is at
        # y_vel -= (y_vel_pos_tr + abs(y_vel_neg_tr))

        # # Move positive velocities up and velocities down
        # tr_y_vel1 = np.pad(y_vel_pos_tr, ((0,2),(0,0)), constant_values=0)
        # tr_y_vel2 = np.pad(y_vel_neg_tr, ((2,0),(0,0)), constant_values=0)

        # # Now add the velocities to the squares where it moved to
        # y_vel_add_vel = tr_y_vel1 + abs(tr_y_vel2)
        # y_vel_add_vel[1,:] += y_vel_add_vel[0,:]
        # y_vel_add_vel[-2,:] += y_vel_add_vel[-1,:]
        # y_vel_add_vel = y_vel_add_vel[1:-1, 0:grid_size]

        # y_vel += y_vel_add_vel

        # Draw the density (higher density = darker)
        draw(dens, x_vel, y_vel)

        # print(np.sum(dens))
        # print(np.sum(x_vel))
        # print(np.sum(y_vel))
        # print('--------------------------')

        # Press "C" to clean entire board
        pg.event.pump()
        keys = pg.key.get_pressed()

        if keys[pg.K_c]:
            dens = np.zeros((grid_size,grid_size))
        
        if keys[pg.K_d]:
            x_vel *= 1.3
            y_vel *= 1.3

# Run
simulate(dens, x_vel, y_vel)




