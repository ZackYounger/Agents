import pygame
from math import *
from random import randint as rand

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
background_colour = (0,0,0)

width,height = 800,800
screen = pygame.display.set_mode((width,height))
screen.fill(background_colour)

agents = []


class Agent:
    def __init__(self, pos=(400,400), angle=pi/2):
        self.pos = pos
        self.speed = 4
        self.angle = angle
        self.look = 50
        self.size = 20
        self.colour = (255,255,255)
    
    def update(self):
        """
        if keys[pygame.K_RIGHT]:
            self.angle += .1
        if keys[pygame.K_LEFT]:
            self.angle -= .1"""
        
        left_view_pos = (cos(20+self.angle)*(self.look+3)+self.pos[0], sin(20+self.angle)*(self.look+3)+self.pos[1])
        right_view_pos = (cos(-20+self.angle)*(self.look+3)+self.pos[0], sin(-20+self.angle)*(self.look+3)+self.pos[1])
        left_view = 0
        right_view = 0
        
        for agent in agents:
            if (left_view_pos[0]-agent.pos[0])**2+(left_view_pos[1]-agent.pos[1])**2 < self.look**2:
                left_view += 1
            if (right_view_pos[0]-agent.pos[0])**2+(right_view_pos[1]-agent.pos[1])**2 < self.look**2:
                right_view +=1
            try: 
                self.angle -= (-left_view/(right_view+left_view)+right_view/(right_view+left_view))*0.001
            except:
                pass
                
        #pygame.draw.circle(screen,(255,0,0),left_view_pos,self.look,1)
        #pygame.draw.circle(screen,(0,0,255),right_view_pos,self.look,1)

        self.pos = (self.pos[0]+cos(self.angle)*self.speed,self.pos[1]+sin(self.angle)*self.speed)

        self.draw()

    def draw(self):
        pos2 = (cos(60+self.angle)*self.size+self.pos[0], sin(60+self.angle)*self.size+self.pos[1])
        pos3 = (cos(-60+self.angle)*self.size+self.pos[0], sin(-60+self.angle)*self.size+self.pos[1])
        pygame.draw.polygon(screen,self.colour,[self.pos, pos2, pos3])


running = True
while running:
    clock.tick(fps_limit)
    screen.fill(background_colour)
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if rand(0,1) == 0:
        agents.append(Agent((rand(25,height-25),-25),radians(rand(80,100))))
    
    for agent in agents:
        agent.update()
        if agent.pos[0] < -25 or agent.pos[1] < -25 or agent.pos[0] > width+25 or agent.pos[1] > height+25:
            agents.remove(agent)
        elif len(agents) > 120:
            agents.remove(agent)
    pygame.display.flip()
pygame.quit()