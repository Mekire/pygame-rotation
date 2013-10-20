import os
import sys
import math
import pygame as pg


class Rotator(object):
    def __init__(self,point,origin):
        self.point = point
        self.origin = origin
        x_mag = point[0]-origin[0]
        y_mag = point[1]-origin[1]
        self.radius = math.hypot(x_mag,y_mag)
        self.start_angle = math.atan2(-y_mag,x_mag)

    def __call__(self,angle):
        new_angle = math.radians(angle)+self.start_angle
        new_x = self.origin[0] + self.radius*math.cos(new_angle)
        new_y = self.origin[1] - self.radius*math.sin(new_angle)
        return (new_x,new_y)


class Character(object):
    def __init__(self,location,origin):
        self.image = pg.image.load("lena_small.png").convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=location)
        self.origin = getattr(self.rect,origin)
        self.rotator = Rotator(self.rect.center,self.origin)
        self.angle = 0

    def rotate(self,surface,speed):
        self.angle = (self.angle+speed)%360
        new_center = self.rotator(self.angle)
        surface.fill((255,255,0),pg.Rect(self.origin,(5,5)))
        self.image = pg.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect(center=new_center)

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def update(self,surface,speed):
        self.rotate(surface,speed)
        self.draw(surface)


class Control(object):
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        pg.init()
        self.screen = pg.display.set_mode((500,500))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.lena_one = Character((250,100),"midbottom")
        self.lena_two = Character((100,400),"topright")

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.screen.fill(0)
            self.lena_one.update(self.screen,1)
            self.lena_two.update(self.screen,1)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
