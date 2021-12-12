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
        self.data["mass"] = (4/3)*(math.pi)*(self.data["radius"]**2)
        self.data["canCollide"] = True
        Planet.planets.append(self)

    def notInEffectiveScreen(self):
        #position is some distance from edge of screen
        xOutOfRange = True if (self.data["position"]["x"] > SETUP.WIDTH + 200 ) or (self.data["position"]["x"] < 0 - 200) else False
        yOutOfRange = True if (self.data["position"]["y"] > SETUP.HEIGHT + 200 ) or (self.data["position"]["y"] < 0 - 200) else False
        
        if xOutOfRange or yOutOfRange:
            return True
   
    @classmethod
    def doCollisions(cls):
       for i, planet in enumerate(Planet.planets):
           if (i != len(Planet.planets) - 1) and planet.data["canCollide"]:
               for otherPlanet in Planet.planets[i+1:]:
                   if planet.collides(otherPlanet) and otherPlanet.data["canCollide"]:
                       print("had a colide mother fuker")
                       planet.doCollision(otherPlanet)

    def wouldBeColliding (self):
        for otherPlanet in Planet.planets:
            if self.collides(otherPlanet):
                print("would collide if you created me")
                return True
            else:
                return False

    def velocity (self):
        return math.sqrt(self.data["velocity"]["x"]**2 + self.data["velocity"]["y"]**2)

    def momentum (self):
        return self.velocity()*self.data["mass"]

    def energy (self):
        return (self.data["mass"]*self.velocity()**2)/2
    
    def doCollision(self, other):
        # I got lazy and got this formula from here: https://ericleong.me/research/circle-circle/
        #use these for testing with initial and final velocities to see if everything is conserved properly
        #totalEnergy = self.energy()+ other.energy() #write an energy method
        #totalMomentum = self.momentum() + other.momentum() #write a momentum method
        pinitial1 = self.momentum()
        pinitial2 = other.momentum()
        pinitialtotal = pinitial1 + pinitial2
        print("inital momentum " + str(pinitialtotal))

        #TODO fix this method so that energy and momentum are actually conserved and not "kinda conserved" right now the system can loose up to like 5% of its momentum in a collision
        distanceBetween = math.sqrt(Planet.distanceBetweenSquared(self, other))
        #n is a unit vector pointing from the center of self to the center of other at the moment they collide
        #This is an approximation because the circles will be a bit over lapping at this point (after all we detected that thier centers were closer than the sum of thier radii)
        #TODO, make this more accurate by finding thier possiions at the actual point of collision (could use time or the method oulined in the link above)
        nx = (self.data["position"]["x"] - other.data["position"]["x"]) / distanceBetween
        ny = (self.data["position"]["y"] - other.data["position"]["y"]) / distanceBetween
        #p is derived from manipulation of Pinitial = Pfinal and KEinitial = KEfinal. It is just a value that relates the velocities of the circles to thier masses
        # p = 2(self.v*n - other.v*n) / ( m1 + m2)
        p = 2 * ((((self.data["velocity"]["x"] - other.data["velocity"]["x"]) * nx) + ((self.data["velocity"]["y"] - other.data["velocity"]["y"]) * ny)))/(1/self.data["mass"] + 1/other.data["mass"])
        #self.vf = initialVelocity - p*mass*unitVector
        #other.vf = initialVelocity + p*mass*unitVector
        vxSelfFinal = self.data["velocity"]["x"] - (p / self.data["mass"]) * nx
        vySelfFinal = self.data["velocity"]["y"] - (p / self.data["mass"]) * ny
        vxOtherFinal = other.data["velocity"]["x"] + (p / other.data["mass"]) * nx
        vyOtherFinal = other.data["velocity"]["y"] + (p / other.data["mass"]) * ny
        #set the values
        self.data["velocity"]["x"] = vxSelfFinal
        self.data["velocity"]["y"] = vySelfFinal
        other.data["velocity"]["x"] = vxOtherFinal
        other.data["velocity"]["y"] = vyOtherFinal
        
        pfinal1 = self.momentum()
        pfinal2 = other.momentum()
        pfinaltotal = pfinal1 + pfinal2
        print("final momentum " + str(pfinaltotal))
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
        result = (planet1.data["position"]["x"] - planet2.data["position"]["x"])**2 + (planet1.data["position"]["y"] - planet2.data["position"]["y"])**2        
        return result

    def updatePosition(self):
        #update x pos
        self.data["position"]["x"] += self.data["velocity"]["x"]
        #update y pos
        self.data["position"]["y"] += self.data["velocity"]["y"]
        #update x and y vel
        #instantaniousDrag = self.drag()
        instantaniousDrag = 0

        self.data["velocity"]["x"] *= (1.0 - instantaniousDrag)
        self.data["velocity"]["y"] *= (1.0 - instantaniousDrag)
        if self.notInEffectiveScreen():
            self.warp()

    def warp(self):
        self.data["canCollide"] = False

        #generate point of pass through - center for now 
        cx = random.randrange(50, SETUP.WIDTH - 50)
        cy = random.randrange(50, SETUP.HEIGHT - 50)

        sx = random.randint(-100, 0)
        sy = random.randint(-100, SETUP.HEIGHT + 100)

        self.data["position"]["x"] = sx 
        self.data["position"]["y"] = sy
        #this will find us a center location that does not collide with anything else
        while self.wouldBeColliding():
            #pick random starting location - only from the left and right for now 
            sx = random.randint(-100, 0)
            sy = random.randint(-100, SETUP.HEIGHT + 100)

            self.data["position"]["x"] = sx 
            self.data["position"]["y"] = sy

        
    
        #distance from start point1 to pass through location
        dc1 = math.sqrt((cx - sx)**2 + (cy - sy)**2)

        #random velocity within range for planet 
        v1mag = random.randrange(2, SETUP.MAXSPEED)
    
        #n is a unit vector from start start point to pass through point
        nx = (cx - sx) / dc1
        ny = (cy - sy) / dc1
    
        #components of unit vector times magnitude of velocity give components of velocity
        xvel = v1mag * nx
        yvel = v1mag * ny

        self.data["velocity"]["x"] = xvel
        self.data["velocity"]["y"] = yvel
        self.data["canCollide"] = True



    def collides(self, other):
        selfNextX = self.data["position"]["x"] + self.data["velocity"]["x"]
        selfNextY = self.data["position"]["y"] + self.data["velocity"]["y"]
        otherNextX = other.data["position"]["x"] + other.data["velocity"]["x"]
        otherNextY = other.data["position"]["y"] + other.data["velocity"]["y"]

        centerDistanceSquared = (self.data["radius"] + other.data["radius"])**2

        distanceBetween = (selfNextX - otherNextX)**2 + (selfNextY - otherNextY)**2 
        #Planet.distanceBetweenSquared(self, other)
        if distanceBetween < centerDistanceSquared:
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
            r =  r1 = random.randrange(20, 100)
            Planet({"radius": r, "position": {"x": xpos, "y": ypos}, "velocity": {"x": xvel, "y": yvel}})
            i+=1
        
    @classmethod
    def generatePlanetsThatWillCollide(cls):

        #random radii
        r1 = random.randrange(20, 100)
        r2 = random.randrange(20, 100)
        #generate point of collision 
        cx = random.randrange(50, SETUP.WIDTH - 50)
        cy = random.randrange(50, SETUP.HEIGHT - 50)
        #pick random starting locations - only from the left and right for now 
        sx1 = random.randint(-50, 0)
        sx2 = random.randint(SETUP.WIDTH, SETUP.WIDTH+50)

        sy1 = random.randint(0, SETUP.HEIGHT)
        sy2 = random.randint(0, SETUP.HEIGHT)
        
        #distance from start point1 to collision location
        dc1 = math.sqrt((cx - sx1)**2 + (cy - sy1)**2)

        #distance from start point2 to collision location
        dc2 = math.sqrt((cx - sx2)**2 + (cy - sy2)**2)

        #random velocity within range for first planet - this will determine how fast the second planet has to move
        v1mag = random.randrange(2, SETUP.MAXSPEED)
        #time to collison d/r =t
        timeToCollision = dc1/v1mag
        #velocity that will make the planet2 arrive at collision site at the same time as planet1 
        v2mag = dc2/timeToCollision
        
        #n is a unit vector from start point1 to collision
        nx = (cx - sx1) / dc1
        ny = (cy - sy1) / dc1
        #a is a unit vector from start point2 to collison
        ax = (cx - sx2) / dc2
        ay = (cy - sy2) / dc2
        #components of unit vector times magnitude of velocity give components of velocity
        xvel1 = v1mag * nx
        yvel1 = v1mag * ny
        xvel2 = v2mag * ax
        yvel2 = v2mag * ay

        return [Planet({"radius": r1, "position": {"x": sx1, "y": sy1}, "velocity": {"x": xvel1, "y": yvel1}}),
        Planet({"radius": r2, "position": {"x": sx2, "y": sy2}, "velocity": {"x": xvel2, "y": yvel2}})]

    @classmethod
    def updatePositions(cls):
        for planet in Planet.planets:
            planet.updatePosition()
        
        
