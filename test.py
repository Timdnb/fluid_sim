import numpy as np
# import random
# import pygame as pg
# import math

# pg.init()

# angle = 90
# white = (255,255,255)

# # Screen
# w_scr = 1000
# h_scr = 1000
# res = (w_scr, h_scr)
# screen = pg.display.set_mode(res)
# screen_rect = screen.get_rect()

# # Arrow image
# arrow = pg.image.load("red_arrow.png")
# arrow_rect = arrow.get_rect()

# arrow = pg.transform.rotate(arrow, angle)

# pg.draw.rect(screen, white, screen_rect)
# screen.blit(arrow, arrow_rect)

# pg.display.flip()

# pg.time.wait(3000)

# pg.quit()

# # y_vel[4,6] = -0.05
# # y_vel[5,6] = -0.05
# # y_vel[6,6] = -0.05
# # y_vel[7,6] = -0.05
# # y_vel[8,6] = -0.05
# # y_vel[9,6] = -0.05
# # y_vel[10,6] = -0.05
# # y_vel[11,6] = -0.05
# # y_vel[12,6] = -0.05
# # y_vel[13,6] = -0.05
# # y_vel[14,6] = -0.05

# # y_vel[6,15] = 0.05
# # y_vel[7,15] = 0.05
# # y_vel[8,15] = 0.05
# # y_vel[9,15] = 0.05
# # y_vel[10,15] = 0.05
# # y_vel[11,15] = 0.05
# # y_vel[12,15] = 0.05
# # y_vel[13,15] = 0.05
# # y_vel[14,15] = 0.05
# # y_vel[15,15] = 0.05
# # y_vel[16,15] = 0.05

# # x_vel[15,6] = 0.05
# # x_vel[15,7] = 0.05
# # x_vel[15,8] = 0.05
# # x_vel[15,9] = 0.05
# # x_vel[15,10] = 0.05
# # x_vel[15,11] = 0.05
# # x_vel[15,12] = 0.05
# # x_vel[15,13] = 0.05
# # x_vel[15,14] = 0.05

# # x_vel[5,7] = -0.05
# # x_vel[5,8] = -0.05
# # x_vel[5,9] = -0.05
# # x_vel[5,10] = -0.05
# # x_vel[5,11] = -0.05
# # x_vel[5,12] = -0.05
# # x_vel[5,13] = -0.05
# # x_vel[5,14] = -0.05
# # # x_vel[5,15] = -0.05

# print(23.16%3)

x_vel = np.zeros((3,3))
x_vel[0,0] = -1
x_vel[1,0] = 0
x_vel[2,0] = 1
x_vel[0,1] = 2
x_vel[1,1] = 1
x_vel[2,1] = -3
x_vel[0,2] = -3
x_vel[1,2] = 2
x_vel[2,2] = 2

x_vel_pos = np.where(x_vel>0, x_vel, 0)
x_vel_neg = np.where(x_vel<0, x_vel, 0)

x_vel1 = np.pad(x_vel_pos, ((0,0),(2,0)), constant_values=0)
x_vel2 = np.pad(x_vel_neg, ((0,0),(0,2)), constant_values=0)



x_vel_add = x_vel1 + abs(x_vel2)

print(x_vel_add)

x_vel_add[:,1] += x_vel_add[:,0]
x_vel_add[:,-2] += x_vel_add[:,-1]

print(x_vel_add)

x_vel_tot = x_vel_add[0:3, 1:-1]

# print(x_vel_tot)

x_vel_final = x_vel_tot - abs(x_vel)

# print(x_vel_final)