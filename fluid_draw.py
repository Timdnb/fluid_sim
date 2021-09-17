import numpy as np
from numpy.lib import c_
import pygame as pg
from math import atan2
from parameters import grid_size

# Pygame
pg.init()

# Screen
w_scr = 1000
h_scr = 1000
res = (w_scr, h_scr)
screen = pg.display.set_mode(res)
screen_rect = screen.get_rect()

# Colors (green -> red)
color1 = (46,127,24)
color2 = (69,115,30)
color3 = (103,94,36)
color4 = (141,71,43)
color5 = (177,52,51)
color6 = (200,37,56)

def draw(dens, x_vel, y_vel, obst, show_vel):
    # White will be assigned to this density
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

            # Draw rectangles and arrows on the screen
            if show_vel == True:
                if obst[row,ele] == False:
                    pg.draw.rect(screen, color, (x, y, w_scr/grid_size, h_scr/grid_size))
                    pg.draw.aaline(screen, color_s, (x+cell_width/2,y+cell_width/2), (x+cell_width/2*(1+np.cos(angle)), y-cell_width/2*(-1+np.sin(angle))))   
                else:
                    pg.draw.rect(screen, (0,0,255), (x, y, w_scr/grid_size, h_scr/grid_size))
            else:
                if obst[row,ele] == False:
                    pg.draw.rect(screen, color, (x, y, w_scr/grid_size, h_scr/grid_size))
                else:
                    pg.draw.rect(screen, (0,0,255), (x, y, w_scr/grid_size, h_scr/grid_size))

    pg.display.flip()
