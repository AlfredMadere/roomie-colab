import pygame
import math
import random
import setup as SETUP

DENSITY = 1

class Planet:
    planets = []
    closePlanets = []
    def __init__(self, data):
        self.data = data
        self.dragCoefficent = SETUP.DRAG
        self.data["mass"] = (4/3)*(math.pi*self.data["radius"]**2)
        Planet.planets.append(self)
   
    @classmethod
    def doCollisions(cls):
       for i, planet in enumerate(Planet.planets):
           print("firs planet", planet)
           if i != len(Planet.planets) - 1:
               for otherPlanet in Planet.planets[i+1:]:
                   print("other planet", otherPlanet)
                   if planet.collides(otherPlanet):
                       print("had a colide mother fuker")
                       planet.doCollision(otherPlanet)
    
    def doCollision(self, other):
        # I got lazy and got this formula from here: https://ericleong.me/research/circle-circle/
        #use these for testing with initial and final velocities to see if everything is conserved properly
        #totalEnergy = self.energy()+ other.energy() #write an energy method
        #totalMomentum = self.momentum() + other.momentum() #write a momentum method
        distanceBetween = math.sqrt(Planet.distanceBetweenSquared(self, other))
        #n is a unit vector pointing from the center of self to the center of other at the moment they collide
        #This is an approximation because the circles will be a bit over lapping at this point (after all we detected that thier centers were closer than the sum of thier radii)
        #TODO, make this more accurate by finding thier possiions at the actual point of collision (could use time or the method oulined in the link above)
        nx = (self.data["position"]["x"] - other.data["position"]["x"]) / distanceBetween
        ny = (self.data["position"]["y"] - other.data["position"]["y"]) / distanceBetween
        #p is derived from manipulation of Pinitial = Pfinal and KEinitial = KEfinal. It is just a value that relates the velocities of the circles to thier masses
        # p = 2(self.v*n - other.v*n) / ( m1 + m2)
        p = 2 * ((self.data["velocity"]["x"] * nx + self.data["velocity"]["y"] * ny) - ((other.data["velocity"]["x"] * nx + other.data["velocity"]["y"] * ny))) / (self.data["mass"] + other.data["mass"])
        #self.vf = initialVelocity - p*mass*unitVector
        #other.vf = initialVelocity + p*mass*unitVector
        vxSelfFinal = self.data["velocity"]["x"] - p * self.data["mass"] * nx
        vySelfFinal = self.data["velocity"]["y"] - p * self.data["mass"] * ny
        vxOtherFinal = other.data["velocity"]["x"] + p * other.data["mass"] * nx
        vyOtherFinal = other.data["velocity"]["y"] + p * other.data["mass"] * ny
        #set the values
        self.data["velocity"]["x"] = vxSelfFinal
        self.data["velocity"]["y"] = vySelfFinal
        other.data["velocity"]["x"] = vxOtherFinal
        other.data["velocity"]["y"] = vyOtherFinal
        
        #This lowkey is such a hack and we should change it, this is because they might still be inside each other after 1 redraw frame... and then it will look like they collided again and we will get weird shit happening
        while Planet.distanceBetweenSquared(self, other) < (self.data["radius"] + other.data["radius"])**2:
            self.updatePosition()
            other.updatePosition()
        
    def drag(self):
        speedsq = math.pow(self.data["velocity"]["x"], 2) + math.pow(self.data["velocity"]["x"], 2)
        return speedsq*self.dragCoefficent

    #Not taking the square root makes things run faster and usally we were gonna compare it to something else we took the square root of anyways.
    @classmethod
    def distanceBetweenSquared(cls, planet1, planet2):
        planet1x = planet1.data["position"]["x"]
        return math.pow(planet1.data["position"]["x"] - planet2.data["position"]["x"], 2) + math.pow(planet1.data["position"]["y"] - planet2.data["position"]["y"], 2)

    def updatePosition(self):
        #update x pos
        self.data["position"]["x"] += self.data["velocity"]["x"]
        #update y pos
        self.data["position"]["y"] += self.data["velocity"]["y"]
        #update x and y vel
        instantaniousDrag = self.drag()
        self.data["velocity"]["x"] *= (1.0 - instantaniousDrag)
        self.data["velocity"]["y"] *= (1.0 - instantaniousDrag)

    def collides(self, other):
        selfNextX = self.data["position"]["x"] + self.data["velocity"]["x"]
        selfNextY = self.data["position"]["y"] + self.data["velocity"]["y"]
        otherNextX = other.data["position"]["x"] + other.data["velocity"]["x"]
        otherNextY = other.data["position"]["y"] + other.data["velocity"]["y"]

        centerDistance = self.data["radius"] + other.data["radius"]

        distanceBetween = math.pow(abs((selfNextX - otherNextX)), 2) - math.pow(abs((selfNextY - otherNextY)), 2)
        if distanceBetween < centerDistance:
            return True

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
        
        
