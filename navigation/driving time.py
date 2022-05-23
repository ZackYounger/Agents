import pygame
from math import *
from random import randint as rand

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
background_colour = (0, 0, 0)

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)

sprite = pygame.image.load('car.png').convert()
#sprite.fill(pygame.Color("red"))
sprite.set_colorkey((246, 246, 246))
mask = pygame.mask.from_surface(sprite)
car_width, car_height = 153, 330
car_scale_factor = 0.5
sprite = pygame.transform.scale(sprite, (round(car_scale_factor*car_width), round(car_scale_factor*car_height)))

class Car:
    def __init__(self, colour=(255, 255, 255)):
        self.inputs = {"forward": pygame.K_UP,
                       "back": pygame.K_DOWN,
                       "right": pygame.K_RIGHT,
                       "left": pygame.K_LEFT}
        self.pos = (width / 2, height / 2)
        self.angle = 90
        self.speed = 0
        self.vel = (0, 0)
        self.colour = colour
        self.drag = 0.97
        self.acc = 0.6
        self.commands = {"forward": False,
                         "back": False,
                         "right": False,
                         "left": False,
                         "r_right": False,
                         "r_left": False,
                         "shoot": False}
        self.scale_factor = 1

        self.original_sprite = sprite
        self.display_sprite = sprite
        self.original_sprite.set_colorkey((246, 246, 246))
        self.display_sprite.set_colorkey((246, 246, 246))
        self.width, self.height = self.original_sprite.get_width(), self.original_sprite.get_height()
        #self.original_sprite = pygame.transform.scale(self.original_sprite, (10, 10))

    def update(self):

        self.commands["forward"] = keys[int(self.inputs["forward"])]
        self.commands["back"] = keys[self.inputs["back"]]
        self.commands["left"] = keys[int(self.inputs["left"])]
        self.commands["right"] = keys[self.inputs["right"]]

        if self.commands["right"]:
            self.angle -= 3
        if self.commands["left"]:
            self.angle += 3

        # if self.vel[0]**2 + self.vel[1]**2 < self.max_speed**2:
        if self.commands["forward"]:
            self.speed -= self.acc
            #self.vel = (
            #self.vel[0] - sin(radians(self.angle)) * self.acc, self.vel[1] - cos(radians(self.angle)) * self.acc)
        if self.commands["back"]:
            self.speed += self.acc
            #self.vel = (
            #self.vel[0] + sin(radians(self.angle)) * self.acc, self.vel[1] + cos(radians(self.angle)) * self.acc)

        # drag:
        self.speed *= self.drag
        self.vel = (sin(radians(self.angle))*self.speed, cos(radians(self.angle))*self.speed)
        #self.vel = (self.vel[0] * self.drag, self.vel[1] * self.drag)

        self.pos = (round(self.pos[0] + self.vel[0]), round(self.pos[1] + self.vel[1]))

        self.display_sprite = pygame.transform.rotozoom(self.original_sprite, self.angle, 1)

        self.draw()


    def draw(self):
        self.display_sprite.set_colorkey((246, 246, 246))
        info = self.display_sprite.get_rect()
        self.display_pos = [self.pos[0] + 40 * sin(radians(self.angle)) + info.width / 2,
                            self.pos[1] + 40 * cos(radians(self.angle)) + info.height / 2]
        screen.blit(self.display_sprite,
                    (self.pos[0] - info.width / 2 + (self.pos[0] - self.display_pos[0]),
                     self.pos[1] - info.height / 2+ (self.pos[1] - self.display_pos[1])))
        #screen.blit(self.display_sprite,
        #            (self.display_pos[0] - info.width / 2 + (self.pos[0] - self.display_pos[0]),
        #             self.display_pos[1] - info.height / 2 + (self.pos[1] - self.display_pos[1])))

        pygame.draw.circle(screen, red, self.pos, 3)
        pygame.draw.circle(screen, red, (self.pos[0] - info.width / 2,
                     self.pos[1] - info.height / 2), 3)
        pygame.draw.circle(screen, red, (self.display_pos[0] - info.width / 2,
                                         self.display_pos[1] - info.height / 2), 3)
        pygame.draw.circle(screen, green, (self.pos[0] - info.width / 2 + (self.display_pos[0] - self.pos[0]),
                     self.pos[1] - info.height/ 2 + (self.display_pos[1] - self.pos[1])), 3)


a = Car()

running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    a.update()

    pygame.display.flip()
pygame.quit()
