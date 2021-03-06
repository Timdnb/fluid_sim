import numpy as np
import pygame as pg
import time
from math import floor

from pygame.surfarray import pixels2d

# Other files
from parameters import grid_size, dens, diff_const_dens, x_vel, y_vel, diff_const_vel, obst, show_vel
from fluid_draw import draw, w_scr, h_scr

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

def simulate(dens, diff_const_dens, x_vel, y_vel, diff_const_vel, show_vel):
    """
    Simulate the whole fluid
    """
    running = True
    n = 0

    while running:
        # time.sleep(1)
        # ------------------------------ Add source(s) -------------------------------------
        # for i in range(8,grid_size-8,3):
        #     dens[i,1] = 40
        #     x_vel[:,1] = 1

        # ------------------------------ Diffusion of density ------------------------------
        dens = diffuse(diff_const_dens, dens)

        # ------------------------------ Diffusion of velocities ---------------------------
        x_vel = diffuse(diff_const_vel, x_vel)
        y_vel = diffuse(diff_const_vel, y_vel)

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

        # ------------------------------ Delete density at edges ---------------------------
        dens[:,0] = 0
        dens[:,-1] = 0
        dens[0,:] = 0
        dens[-1,:] = 0

        # ------------------------------ Clearing divergence -------------------------------
        x_vel_div1 = np.pad(x_vel, ((0,0),(2,0)), constant_values=0)
        x_vel_div2 = np.pad(x_vel, ((0,0),(0,2)), constant_values=0)

        x_vel_div_tot = x_vel_div2 - x_vel_div1
        x_vel_div_tot = x_vel_div_tot[0:grid_size, 1:-1]

        y_vel_div1 = np.pad(y_vel, ((0,2),(0,0)), constant_values=0)
        y_vel_div2 = np.pad(y_vel, ((2,0),(0,0)), constant_values=0)

        y_vel_div_tot = y_vel_div2 - y_vel_div1
        y_vel_div_tot = y_vel_div_tot[1:-1, 0:grid_size]

        div = (x_vel_div_tot + y_vel_div_tot) / 2

        p = np.zeros((grid_size,grid_size))

        for k in range(20):
            for i in range(1,grid_size-1):
                for j in range(1,grid_size-1):
                    p[i,j] = (p[i-1,j] + p[i+1,j] + p[i,j-1] + p[i,j+1] - div[i,j]) / 4
        
        px1 = np.pad(p, ((0,0),(2,0)), constant_values=0)
        px2 = np.pad(p, ((0,0),(0,2)), constant_values=0)

        py1 = np.pad(p, ((0,2),(0,0)), constant_values=0)
        py2 = np.pad(p, ((2,0),(0,0)), constant_values=0)

        px = (px2 - px1) / 2
        py = (py2 - py1) / 2

        px = px[0:grid_size,1:-1]
        py = py[1:-1,0:grid_size]

        x_vel -= px
        y_vel -= py

        # ------------------------------ Self-Advection of velocities ----------------------
        # X-velocity
        # Separate positive and negative x-velocities
        x_vel_pos = np.where(x_vel>0, x_vel, 0)
        x_vel_neg = np.where(x_vel<0, x_vel, 0)

        # Calculate velocity that will be moved away
        x_vel_pos_tr = -(1/(1+np.exp(x_vel_pos))-0.5)*0.05 #*x_vel_pos
        x_vel_neg_tr = -(1/(1+np.exp(x_vel_neg))-0.5)*0.05 #*x_vel_neg

        # Subtract this velocity from the squares where it is at
        x_vel -= (x_vel_pos_tr + abs(x_vel_neg_tr))

        # Move positive velocities to the right and negative to the left
        tr_x_vel1 = np.pad(x_vel_pos_tr, ((0,0),(2,0)), constant_values=0)
        tr_x_vel2 = np.pad(x_vel_neg_tr, ((0,0),(0,2)), constant_values=0)

        # Now add the velocities to the squares where it moved to
        x_vel_add_vel = tr_x_vel1 + abs(tr_x_vel2)
        x_vel_add_vel[:,1] += x_vel_add_vel[:,0]
        x_vel_add_vel[:,-2] += x_vel_add_vel[:,-1]
        x_vel_add_vel = x_vel_add_vel[0:grid_size, 1:-1]

        x_vel += x_vel_add_vel

        # Y-velocity
        # Separate positive and negative y-velocities
        y_vel_pos = np.where(y_vel>0, y_vel, 0)
        y_vel_neg = np.where(y_vel<0, y_vel, 0)

        # Calculate velocity that will be moved away
        y_vel_pos_tr = -(1/(1+np.exp(y_vel_pos))-0.5)*0.05 #y_vel_pos
        y_vel_neg_tr = -(1/(1+np.exp(y_vel_neg))-0.5)*0.05 #y_vel_neg

        # Subtract this velocity from the squares where it is at
        y_vel -= (y_vel_pos_tr + abs(y_vel_neg_tr))

        # Move positive velocities up and velocities down
        tr_y_vel1 = np.pad(y_vel_pos_tr, ((0,2),(0,0)), constant_values=0)
        tr_y_vel2 = np.pad(y_vel_neg_tr, ((2,0),(0,0)), constant_values=0)

        # Now add the velocities to the squares where it moved to
        y_vel_add_vel = tr_y_vel1 + abs(tr_y_vel2)
        y_vel_add_vel[1,:] += y_vel_add_vel[0,:]
        y_vel_add_vel[-2,:] += y_vel_add_vel[-1,:]
        y_vel_add_vel = y_vel_add_vel[1:-1, 0:grid_size]

        y_vel += y_vel_add_vel

        # Draw the density (higher density = darker)
        draw(dens, x_vel, y_vel, obst, show_vel)

        # ------------------------------ Obstacles properties -------------------------------
        # If there is a obstacle present, multiply velocity with -1 (boundary condition)
        x_vel = np.where(obst, x_vel*-1, x_vel)
        y_vel = np.where(obst, y_vel*-1, y_vel)
        
        # ------------------------------ Controls -------------------------------------------
        # Get keys pressed information
        pg.event.pump()
        keys = pg.key.get_pressed()

        # Add walls using 1,2,3,4 keys
        if keys[pg.K_1]:
            x_vel[:,0] = -x_vel[:,1]
            obst[:,0] = True

        if keys[pg.K_2]:
            y_vel[0,:] = -y_vel[1,:]
            obst[0,:] = True

        if keys[pg.K_3]:
            x_vel[:,-1] = -x_vel[:,-2]
            obst[:,-1] = True

        if keys[pg.K_4]:
            y_vel[-1,:] = -y_vel[-2,:]
            obst[-1,:] = True

        # Press escape to exit simulation
        if keys[pg.K_ESCAPE]:
            exit()

        # Press "C" to clean entire board
        if keys[pg.K_c]:
            dens = np.zeros((grid_size,grid_size))
        
        # Press "D" to increase velocities by factor 1.3
        if keys[pg.K_d]:
            x_vel *= 1.3
            y_vel *= 1.3
        
        # Press space to pause simulation
        if keys[pg.K_SPACE]:
            pg.time.wait(200)
            pause = True
            while pause:
                pg.event.pump()
                keys = pg.key.get_pressed()

                if keys[pg.K_SPACE]:
                    pg.time.wait(200)
                    break

        # Press "I" to get information about flow          
        if keys[pg.K_i]:
            print(np.sum(dens))
            print(np.sum(x_vel))
            print(np.sum(y_vel))
            print('--------------------------')
        
        # Toggle velocity field
        if keys[pg.K_h]:
            if n % 2 == 0:
                show_vel = False
            else:
                show_vel = True
            n += 1
            pg.time.wait(200)
        
        # Get mouse position information
        mouse = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()

        # Click with LMB to add density and velocity
        if mouse==(1,0,0):
            ele = floor(mouse_pos[0] / (w_scr/grid_size))
            row = floor(mouse_pos[1] / (h_scr/grid_size))

            dens[row,ele] += 40

            # for i in range(3):
                # x_vel[row-1+i,ele] *= 1.1
                # x_vel[row,ele-1+i] *= 1.1
                # y_vel[row-1+i,ele] *= 1.1 
                # y_vel[row,ele-1+i] *= 1.1

        # Click with RMB to add a obstacle
        if mouse==(0,0,1):
            ele = floor(mouse_pos[0] / (w_scr/grid_size))
            row = floor(mouse_pos[1] / (h_scr/grid_size))

            obst[row,ele] = True
        
# Run
simulate(dens, diff_const_dens, x_vel, y_vel, diff_const_vel, show_vel)




