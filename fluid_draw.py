import numpy as np
from numpy.lib import c_
import pygame as pg
from math import atan2, floor
from parameters import grid_size

# Pygame
pg.init()

# Screen
w_scr = 1000
h_scr = 1000
res = (w_scr, h_scr)
screen = pg.display.set_mode(res)
screen_rect = screen.get_rect()

# Arrow image
arrow = pg.image.load("red_arrow.png")
arrow_rect = arrow.get_rect()

# Colors (green -> red)
color1 = (46,127,24)
color2 = (69,115,30)
color3 = (103,94,36)
color4 = (141,71,43)
color5 = (177,52,51)
color6 = (200,37,56)

def draw(dens, x_vel, y_vel):
    pg.event.pump()

    # Press escape to exit simulation
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        exit()

    # Press space to pause the simulation for 3 seconds
    if keys[pg.K_SPACE]:
        pg.time.wait(3000)

    # Click with the mouse to add density and velocity
    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    if mouse==(1,0,0) or mouse==(1,1,0):
        ele = floor(mouse_pos[0] / (w_scr/grid_size))
        row = floor(mouse_pos[1] / (h_scr/grid_size))

        dens[row,ele] += 20

        # Give the 4 surrounding squares velocity to spread
        # y_vel[row-1,ele] += 0.8
        # y_vel[row+1,ele] -= 0.8
        # x_vel[row,ele-1] -= 0.8
        # x_vel[row,ele+1] += 0.8

    # Find max density, black will be assigned to this density
    max_dens = 50

    # Draw rectangles and arrows
    for row in range(grid_size):
        for ele in range(grid_size):
            x = ele*(w_scr/grid_size)
            y = row*(h_scr/grid_size)

            cell_width = w_scr/grid_size

            # Make color based on density (lower density = lighter color)
            c_dens = int((dens[row,ele]/max_dens)*255) 
            if c_dens < 0:
                c_dens = 0  
            if c_dens > 255:
                c_dens = 255      
            color = pg.Color(c_dens,c_dens,c_dens)

            # Position arrow
            arrow_rect.x = x
            arrow_rect.y = y

            # Calculate angle for velocity vector
            angle = atan2(y_vel[row,ele],x_vel[row,ele]) #* (180/np.pi)   
            speed = (y_vel[row,ele]**2 + x_vel[row,ele]**2) ** (1/2)

            if speed >= 0:
                color_s = color1
            if speed > 0.16:
                color_s = color2
            if speed > 0.32:
                color_s = color3
            if speed > 0.49:
                color_s = color4
            if speed > 0.65:
                color_s = color4
            if speed > 0.91:
                color_s = color5
            if speed > 0.99:
                color_s = color6 

            # # Resize and rotate
            # arrow_siz = pg.transform.smoothscale(arrow, (int(0.7*(w_scr/grid_size)),int(0.7*(h_scr/grid_size))))
            # arrow_ang = pg.transform.rotate(arrow_siz, angle)

            # Draw rectangles and blit arrow on the screen
            pg.draw.rect(screen, color, (x, y, w_scr/grid_size, h_scr/grid_size))
            pg.draw.aaline(screen, color_s, (x+cell_width/2,y+cell_width/2), (x+cell_width/2*(1+np.cos(angle)), y-cell_width/2*(-1+np.sin(angle))))
            # pg.draw.circle(screen, color_s, (x+cell_width/2*(1.2+np.cos(angle)), y-cell_width/2*(-1.2+np.sin(angle))), 2)
            # pg.draw.circle(screen, color_s, (x+cell_width/2,y+cell_width/2), 1)

            # screen.blit(arrow_ang, arrow_rect)

    pg.display.flip()
