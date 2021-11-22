import pygame
import math
import random
import setup as SETUP

class Planet:
    planets = []
    def __init__(self, data):
        self.data = data
        self.dragCoefficent = SETUP.DRAG
        Planet.planets.append(self)

    def drag(self):
        speedsq = math.pow(self.data["velocity"]["x"], 2) + math.pow(self.data["velocity"]["x"], 2)
        return speedsq*self.dragCoefficent

    def updatePosition(self):
        #update x pos
        self.data["position"]["x"] += self.data["velocity"]["x"]
        #update y pos
        self.data["position"]["y"] += self.data["velocity"]["y"]
        #update x and y vel
        instantaniousDrag = self.drag()
        self.data["velocity"]["x"] *= (1.0 - instantaniousDrag)
        self.data["velocity"]["y"] *= (1.0 - instantaniousDrag)


    def render(self, surface):
        pygame.draw.circle(surface, (0,0,0), (self.data["position"]["x"],self.data["position"]["y"]), self.data["radius"])

    @classmethod
    def generatePlanets(cls, count):
        i = 0
        while i<count:
            xpos = random.randrange(0, SETUP.WIDTH)
            ypos = random.randrange(0, SETUP.HEIGHT)
            xvel = random.randrange(-SETUP.MAXSPEED, SETUP.MAXSPEED)
            yvel = random.randrange(-SETUP.MAXSPEED, SETUP.MAXSPEED)
            Planet({"radius": 50, "position": {"x": xpos, "y": ypos}, "velocity": {"x": xvel, "y": yvel}})
            i+=1

    @classmethod
    def updatePositions(cls):
        for planet in Planet.planets:
            planet.updatePosition()
        
        
