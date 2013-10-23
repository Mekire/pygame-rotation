"""
Demonstrates rotation of an image around a specified origin.
Change axis of rotation with left mouse button.
Arrow keys for linear movement.
0, -, and + keys to stop, decrease, and increase rotation speed.

-Written by Sean J. McKiernan
"""

import os
import sys
import math
import pygame as pg


DIRECT_DICT = {pg.K_LEFT  : (-1, 0),
               pg.K_RIGHT : ( 1, 0),
               pg.K_UP    : ( 0,-1),
               pg.K_DOWN  : ( 0, 1)}


class Rotator(object):
    def __init__(self,center,origin,image_angle=0):
        x_mag = center[0]-origin[0]
        y_mag = center[1]-origin[1]
        self.radius = math.hypot(x_mag,y_mag)
        self.start_angle = math.atan2(-y_mag,x_mag)-math.radians(image_angle)

    def __call__(self,angle,origin):
        new_angle = math.radians(angle)+self.start_angle
        new_x = origin[0] + self.radius*math.cos(new_angle)
        new_y = origin[1] - self.radius*math.sin(new_angle)
        return (new_x,new_y)


class Character(object):
    def __init__(self,image,location,origin="center"):
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=location)
        self.angle = 0
        try:
            self.set_origin(getattr(self.rect,origin))
        except TypeError:
            self.set_origin(origin)
        self.speed = 3
        self.speed_ang = 1
        self.player_control = False

    def set_origin(self,point):
        self.origin = list(point)
        self.rotator = Rotator(self.rect.center,point,self.angle)

    def rotate(self):
        if self.speed_ang:
            self.angle = (self.angle+self.speed_ang)%360
            new_center = self.rotator(self.angle,self.origin)
            self.image = pg.transform.rotate(self.original_image,self.angle)
            self.rect = self.image.get_rect(center=new_center)

    def draw(self,surface,draw_origin=False):
        surface.blit(self.image,self.rect)
        if draw_origin:
            pg.draw.circle(surface,(255,0,255),self.origin,4)

    def move(self,keys):
        for key in DIRECT_DICT:
            if keys[key]:
                for i in (0,1):
                    change = DIRECT_DICT[key][i]*self.speed
                    self.origin[i] += change
                    self.rect[i] += change

    def update(self,surface,keys):
        if self.player_control:
            self.move(keys)
        self.rotate()
        self.draw(surface,draw_origin=True)


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.actor = Character(LENA,self.screen_rect.center,"midbottom")
        self.actor.player_control = True

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actor.set_origin(event.pos)
            elif event.type == pg.KEYDOWN:
                if event.key in (pg.K_EQUALS,pg.K_KP_PLUS):
                    self.actor.speed_ang += 1
                elif event.key in (pg.K_MINUS,pg.K_KP_MINUS):
                    self.actor.speed_ang -= 1
                elif event.key in (pg.K_0,pg.K_KP0):
                    self.actor.speed_ang = 0

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(0)
            self.actor.update(self.screen,self.keys)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pg.init()
    pg.display.set_mode((500,500))
    LENA = pg.image.load("lena_small.png").convert_alpha()
    LOGO = pg.image.load("pyforum_logo.png").convert_alpha()
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
