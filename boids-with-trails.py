import pygame
from math import *
from random import randint as rand

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

background_colour = white

width, height = 900, 900
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)

background_rect = pygame.Rect(0, 0, width, height)

agents = []


class Boid():
    def __init__(self):
        self.pos = [width - 300, height / 2]
        self.angle = -3
        self.speed = 3
        self.hsv_value = 0
        self.size = 15
        self.colour = (125,40,180)
        self.no_tracers = 21  # should be odd
        self.look_distance = 100
        self.look_max_angle = radians(150)
        self.saved_point = (0, 0)
        self.saved_tracer = 1
        self.arc_rect = (0,0,0,0)
        self.home_colour = black
        self.path =[]
        self.no_colour_inspections = 5

    def update(self):

        self.draw()

        delta_angle = 0

        viewpoint = (self.pos[0] + cos(self.angle) * self.look_distance,
                     self.pos[1] + sin(self.angle) * self.look_distance)

        for tracer in range(self.saved_tracer, self.no_tracers + 1):
            look_angle = self.angle + (2 * self.look_max_angle / (self.no_tracers - 1)) * (
                    (tracer // 2) * (tracer % 2 * 2 - 1))
            inspected_point = (
            round(viewpoint[0] + self.look_distance * cos(look_angle)),
            round(viewpoint[1] + self.look_distance * sin(look_angle)))

            unit = ((inspected_point[0] - viewpoint[0]) / self.no_colour_inspections,
                    (inspected_point[1] - viewpoint[1]) / self.no_colour_inspections)

            if 0 < inspected_point[0] < width and 0 < inspected_point[1] < height:
                if all(screen.get_at((int(viewpoint[0] + unit[0] * i), int(viewpoint[1] + unit[1] * i)))[:3] == self.home_colour for i in range(1, self.no_colour_inspections + 1)):
                    if tracer != self.saved_tracer:
                        self.saved_point = inspected_point
                        self.saved_tracer = tracer
                        self.arc_rect = pygame.Rect(self.saved_point[0] - 20, self.saved_point[1] - 20, 40, 40)
                    pygame.draw.line(screen, green, viewpoint, inspected_point)
                    delta_angle = (look_angle - self.angle) * self.speed / 185
                    for i in range(1, self.no_colour_inspections + 1):
                        pygame.draw.circle(screen, blue, (viewpoint[0] + unit[0] * i, viewpoint[1] + unit[1] * i), 3)

                    break
            pygame.draw.line(screen, red, viewpoint, inspected_point)

        if delta_angle != 0 and self.arc_rect.collidepoint(self.pos):
            self.saved_tracer = 1

        pygame.draw.rect(screen, red, self.arc_rect, 2)
        pygame.draw.circle(screen, red, self.saved_point, 5)
        pygame.draw.line(screen, red, self.pos, viewpoint)

        self.angle += delta_angle
        self.pos = (self.pos[0] + cos(self.angle) * self.speed,
                    self.pos[1] + sin(self.angle) * self.speed)

        self.path.append(self.pos)


    def draw(self):
        pos2 = (cos(60 + self.angle) * self.size + self.pos[0], sin(60 + self.angle) * self.size + self.pos[1])
        pos3 = (cos(-60 + self.angle) * self.size + self.pos[0], sin(-60 + self.angle) * self.size + self.pos[1])
        pygame.draw.polygon(screen, self.colour, [self.pos, pos2, pos3])

        for i, segment in enumerate(self.path):
            if i != 0:
                pygame.draw.line(screen, green, self.path[i-1], segment, 15)


a = Boid()

running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    pygame.draw.rect(screen, black, (50, 50, width - 100, height - 100))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    a.update()

    pygame.display.flip()
pygame.quit()
