import pygame as pg
from matrix_functions import *
from math import sqrt

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.wTc = np.eye(4)
        self.wTc[3,:3] = position
        self.cTw = np.linalg.pinv(self.wTc.T)

        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.5
        self.rotation_speed = 0.02

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.cTw[0,3] -= self.moving_speed # position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.cTw[0,3] += self.moving_speed
        if key[pg.K_w]:
            self.cTw[2,3] += self.moving_speed
        if key[pg.K_s]:
            self.cTw[2,3] -= self.moving_speed
        if key[pg.K_q]:
            self.cTw[1,3] += self.moving_speed
        if key[pg.K_e]:
            self.cTw[1,3] -= self.moving_speed


        if key[pg.K_LEFT]:
            self.rotate_camera(self.rotation_speed, 'y')
        if key[pg.K_RIGHT]:
            self.rotate_camera(-self.rotation_speed, 'y')
        if key[pg.K_UP]:
            self.rotate_camera(self.rotation_speed, 'x')
        if key[pg.K_DOWN]:
            self.rotate_camera(-self.rotation_speed, 'x')

        if key[pg.K_PERIOD]:
            self.rotate_camera(self.rotation_speed,'z')
        if key[pg.K_COMMA]:
            self.rotate_camera(-self.rotation_speed, 'z')

        self.wTc = np.linalg.pinv(self.cTw).T

    def mouse_control(self, pos):
        if pos[0] != 0:
            self.rotate_camera(-pos[0] / 400, 'y')
        if pos[1] != 0:
            self.rotate_camera(-pos[1] / 400, 'x')

    def rotate_camera(self, angle, axis):
        if (axis == 'y'):
            rotate_in_cTw = rotate_y(angle)
        elif (axis == 'x'):
            rotate_in_cTw = rotate_x(angle)
        elif (axis == 'z'):
            rotate_in_cTw = rotate_z(angle)
        else:
            rotate_in_cTw = np.eye(4)

        self.cTw = self.cTw @ rotate_in_cTw

    # def camera_yaw(self, angle):
    #     self.rotate_camera(angle, 'y')

    # def camera_pitch(self, angle):
    #     self.rotate_camera(angle, 'x')

    # def camera_z(self, angle):
    #     self.rotate_camera(angle, 'z')

    # def translate_matrix(self):
    #     x, y, z, w = self.position
    #     return np.array([
    #         [1, 0, 0, 0],
    #         [0, 1, 0, 0],
    #         [0, 0, 1, 0],
    #         [-x, -y, -z, 1]
    #     ])

    # def rotate_matrix(self):
    #     rx, ry, rz, w = self.right
    #     fx, fy, fz, w = self.forward
    #     ux, uy, uz, w = self.up
    #     return np.array([
    #         [rx, ux, fx, 0],
    #         [ry, uy, fy, 0],
    #         [rz, uz, fz, 0],
    #         [0, 0, 0, 1]
    #     ])

    def camera_matrix(self):
        return self.wTc
