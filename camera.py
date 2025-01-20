import pygame as pg
from matrix_functions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.5
        self.rotation_speed = 0.02

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

        if key[pg.K_PERIOD]:
            self.camera_z(-self.rotation_speed)
        if key[pg.K_COMMA]:
            self.camera_z(self.rotation_speed)

    def rotate_camera(self, angle, axis):
        wTc = self.camera_matrix().T
        cTw = np.linalg.pinv(wTc)
        if (axis == 'y'):
            rotate_in_cTw = rotate_y(angle)
        elif (axis == 'x'):
            rotate_in_cTw = rotate_x(angle)
        elif (axis == 'z'):
            rotate_in_cTw = rotate_z(angle)
        else:
            rotate_in_cTw = np.eye(4)

        rotated_cTw = cTw @ rotate_in_cTw
        rotated_wTc = np.linalg.pinv(rotated_cTw).T
        self.forward = rotated_wTc[:,2]
        self.right = rotated_wTc[:,0]
        self.up = rotated_wTc[:,1]
        self.forward[-1] = 1
        self.right[-1] = 1
        self.up[-1] = 1


    def camera_yaw(self, angle):
        self.rotate_camera(angle, 'y')

    def camera_pitch(self, angle):
        self.rotate_camera(angle, 'x')

    def camera_z(self, angle):
        self.rotate_camera(angle, 'z')

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
