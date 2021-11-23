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
        #if notInScreen:
         #   self.warp()
         
    def warp():
        #pick random point and random velocity inside canvas
        #do math to figure out where that would have had to start outside canvas
        #Needs to check if relocating to be colliding, pick new location if colliding
        pass

    def collides(self, other):
        selfNextX = self.data["position"]["x"] + self.data["velocity"]["x"]
        selfNextY = self.data["position"]["y"] + self.data["velocity"]["y"]
        otherNextX = other.data["position"]["x"] + other.data["velocity"]["x"]
        otherNextY = other.data["position"]["y"] + other.data["velocity"]["y"]

        centerDistance = self.data["radius"] + other.data["radius"]

        distanceBetween = math.pow(abs((selfNextX - otherNextX)), 2) - math.pow(abs((selfNextY - otherNextY)), 2)
        if distanceBetween < centerDistance:
            return True

    def doCollision(self, other): #TODO
        pass

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
        
        
