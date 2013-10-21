"""
Demonstrates rotation of an image around a specified origin.

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
    def __init__(self,point,origin):
        x_mag = point[0]-origin[0]
        y_mag = point[1]-origin[1]
        self.radius = math.hypot(x_mag,y_mag)
        self.start_angle = math.atan2(-y_mag,x_mag)

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
        try:
            self._origin = list(getattr(self.rect,origin))
        except TypeError:
            self._origin = list(origin)
        self.rotator = Rotator(self.rect.center,self.origin)
        self.angle = 0
        self.speed = 3
        self.player_control = False

    @property
    def origin(self):
        return self._origin
    @origin.setter
    def origin(self,new_origin):
        offset = [0,0]
        offset[0] = new_origin[0]-self._origin[0]
        offset[1] = new_origin[1]-self._origin[1]
        self.rect.move_ip(offset)
        self._origin = new_origin

    def rotate(self,surface,speed):
        self.angle = (self.angle+speed)%360
        new_center = self.rotator(self.angle,self.origin)
        self.image = pg.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=new_center)

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self,keys):
        if self.player_control:
            for key in DIRECT_DICT:
                if keys[key]:
                    self.origin[0] += DIRECT_DICT[key][0]*self.speed
                    self.origin[1] += DIRECT_DICT[key][1]*self.speed

    def update(self,surface,speed,keys):
        self.move(keys)
        self.rotate(surface,speed)
        self.draw(surface)
        origin_rect = pg.Rect(0,0,6,6)
        origin_rect.center = self.origin
        surface.fill((255,0,255),origin_rect)


class Control(object):
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.actor_one = Character(LOGO,(100,100),"midbottom")
        self.actor_one.player_control = True
        self.actor_two = Character(LENA,(300,300),(270,280))

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(0)
            self.actor_two.update(self.screen,-2,self.keys)
            self.actor_one.update(self.screen,1,self.keys)
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
