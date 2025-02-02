from object_3d import *
import pygame as pg
from camera import *
from projection import *
from sys import argv
from os.path import expanduser

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.fullscreen = False
        self.exit_window = False
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.set_pos = (800, 450)

    def create_objects(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = self.get_object_from_file(expanduser(argv[1]))
        #self.world_axes = Axes(self)
        #self.world_axes.movement_flag = False
        #self.world_axes.scale(20)
        #self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill((0, 0, 0))
        #self.world_axes.draw()
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            if not self.exit_window:
                pg.mouse.set_pos = (800, 450)
            self.camera.control()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif not self.exit_window and event.type == pg.MOUSEMOTION:
                    self.camera.mouse_control(event.rel)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_F11:
                        if self.fullscreen:
                            self.screen = pg.display.set_mode(self.RES, pg.RESIZABLE)
                            self.fullscreen = False
                        else:
                            self.screen = pg.display.set_mode(self.RES, pg.FULLSCREEN)
                            self.fullscreen = True
                    elif event.key == pg.K_ESCAPE:
                        self.exit_window = True
                        pg.mouse.set_visible(True)
                        pg.event.set_grab(False)
            pg.display.set_caption(f'{self.clock.get_fps():.3f}')
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = SoftwareRender()
    app.run()
