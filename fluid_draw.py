import numpy as np
import pygame as pg
from math import atan2, floor
from parameters import grid_size, dens, x_vel, y_vel, show_arrows

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

# Create transparant surface to blit arrows on
arrows = pg.Surface(res, pg.SRCALPHA, 32)
arrows = arrows.convert_alpha()
arrows_rect = arrows.get_rect()

# Draw arrows
if show_arrows:
    for row in range(grid_size):
        for ele in range(grid_size):
            # Position arrow
            arrow_rect.x = ele*(w_scr/grid_size)
            arrow_rect.y = row*(h_scr/grid_size)

            # Calculate angle for velocity vector
            angle = atan2(y_vel[row,ele],x_vel[row,ele]) * (180/np.pi)

            # Resize and rotate
            arrow_siz = pg.transform.smoothscale(arrow, (int(0.7*(w_scr/grid_size)),int(0.7*(h_scr/grid_size))))
            arrow_ang = pg.transform.rotate(arrow_siz, angle)

            # Blit onto surface
            arrows.blit(arrow_ang, arrow_rect)

def draw(dens):
    # Press escape to exit simulation
    pg.event.pump()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        exit()
    
    if keys[pg.K_SPACE]:
        pg.time.wait(3000)

    # Click with the mouse to add density
    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    if mouse==(1,0,0) or mouse==(1,1,0):
        ele = floor(mouse_pos[0] / (w_scr/grid_size))
        row = floor(mouse_pos[1] / (h_scr/grid_size))

        dens[row,ele] += 250

    # Find max density, black will be assigned to this density
    max_dens = 50 # np.max(dens) + 0.0001

    # Draw rectangles and arrows
    for row in range(grid_size):
        for ele in range(grid_size):
            x = ele*(w_scr/grid_size)
            y = row*(h_scr/grid_size)

            # Make color based on density (lower density = lighter color)
            c_dens = 255 - int((dens[row,ele]/max_dens)*255) 
            if c_dens < 0:
                c_dens = 0        
            color = (c_dens,c_dens,c_dens)

            # Draw rectangles and blit arrow on the screen
            pg.draw.rect(screen, color, (x, y, w_scr/grid_size, h_scr/grid_size))

    screen.blit(arrows, arrows_rect)

    pg.display.flip()