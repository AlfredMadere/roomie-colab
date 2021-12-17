import pygame
import math
import random

from pygame.constants import CONTROLLER_AXIS_INVALID
import setup as SETUP

DENSITY = 1

class Planet(pygame.sprite.Sprite):
    minRadius, maxRadius = [50, 100]
    planets = []
    planetStyles = {
        "bigPlanets": ["./planet-game/assets/planets/green_planet.png"],
        "mediumPlanets": ["./planet-game/assets/planets/orange_planet.png"],
        "smallPlanets": ["./planet-game/assets/planets/volcano_planet.png"],
        "miscPlanets": ["./planet-game/assets/planets/stripey_brown.png"]
    }
    closePlanets = []
    def __init__(self, data):
        pygame.sprite.Sprite.__init__(self)
        #TODO: update so that there is no "data" attribute with all the data, that is stupid. Just make them all the data members, attributes of the class
        self.data = data
        self.dragCoefficent = SETUP.DRAG
        self.data["mass"] = (4/3)*(math.pi)*(self.data["radius"]**2)
        self.data["canCollide"] = True
        self.data["color"] = (0,0,0)
        self.image = pygame.transform.scale(pygame.image.load(self.getPlanetStyle()).convert_alpha(), (self.data["radius"]*2, self.data["radius"]*2))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.data["position"]["x"]
        self.rect.centery = self.data["position"]["y"]
        self.pos = pygame.Vector2(self.data["position"]["x"], self.data["position"]["y"])
        self.velocity = pygame.math.Vector2(self.data["velocity"]["x"], self.data["velocity"]["y"])
        self.momentum = self.velocity*self.data["mass"]
        self.energy = .5*self.data["mass"]*self.velocity.magnitude()**2
        Planet.planets.append(self)

    def getPlanetStyle(self):
        #TODO this is a dumb way to select sizes of planets, use difference in range instead
        r = self.data["radius"]
        if r > Planet.maxRadius*.8:
            return Planet.planetStyles["bigPlanets"][random.randint(0, len(Planet.planetStyles["bigPlanets"]) - 1)]
        elif r > Planet.maxRadius*.4 and r < Planet.maxRadius *.8 :
            return Planet.planetStyles["mediumPlanets"][random.randint(0, len(Planet.planetStyles["mediumPlanets"]) - 1)]
        elif r > Planet.minRadius and r < Planet.maxRadius*.4:
            return Planet.planetStyles["smallPlanets"][random.randint(0, len(Planet.planetStyles["smallPlanets"]) - 1)]
        else:
            print("planet size out of range")
            return Planet.planetStyles["smallPlanets"][0]

    def notInEffectiveScreen(self):
        buffer = 200
        xOutOfRange = True if (self.data["position"]["x"] > SETUP.WIDTH + buffer ) or (self.data["position"]["x"] < 0 -  buffer) else False
        yOutOfRange = True if (self.data["position"]["y"] > SETUP.HEIGHT + buffer ) or (self.data["position"]["y"] < 0 - buffer) else False
        
        if xOutOfRange or yOutOfRange:
            return True
   
    @classmethod
    def doCollisions(cls):
        for i, planet in enumerate(Planet.planets):
           if (i != len(Planet.planets) - 1) and planet.data["canCollide"]:
               for otherPlanet in Planet.planets[i+1:]:
                   if planet.collides(otherPlanet) and otherPlanet.data["canCollide"]:
                       planet.doCollision(otherPlanet)

    def wouldBeCollidingSoon (self):
        #detects if a planet is near another planet (not actually if it's colling soon)
        #TODO: change name to nearOtherPlanet
        for otherPlanet in Planet.planets:
            if self != otherPlanet:
                if self.nearlyOverlaps(otherPlanet):
                    print("would be *almost* overlapping if you created me")
                    return True
                else:
                    return False

    def nearlyOverlaps (self, other):
        buffer = 50
        return Planet.distanceBetweenSquared(self, other) < (self.data["radius"] + other.data["radius"] + buffer)**2 
    
    def doCollision(self, other):
        
        # I got lazy and got this formula from here: https://ericleong.me/research/circle-circle/
        #use these for testing with initial and final velocities to see if everything is conserved properly
        pinitial1 = self.momentum
        pinitial2 = other.momentum
        einitialtotal = self.energy + other.energy
        pinitialtotal = pinitial1 + pinitial2

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
        
        pfinal1 = self.momentum
        pfinal2 = other.momentum
        pfinaltotal = pfinal1 + pfinal2
        pdiffmag = (pinitialtotal - pfinaltotal).magnitude()
        efinaltotal = self.energy + other.energy

        #this doesn't ever seem to be a problem
        if pdiffmag>pinitialtotal.magnitude()/10000:
            print("momentum was not conserved, diff: " + str(pdiffmag))
            self.data["color"] = (0, 255, 0)
            other.data["color"] = (0, 255, 0)
        else: 
            print("momentum was conserved, diff: " + str(pdiffmag))
        if abs(einitialtotal - efinaltotal)>einitialtotal/10000:
            print("energy was not conserved, diff: " + str(einitialtotal-efinaltotal))
            self.data["color"] = (0, 0, 255)
            other.data["color"] = (0, 0, 255)
        else: 
            print("energy was conserved, diff: " + str(einitialtotal-efinaltotal))

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
        result = ((planet1.data["position"]["x"] - planet2.data["position"]["x"])**2 + (planet1.data["position"]["y"] - planet2.data["position"]["y"])**2)        
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

        if self.notInEffectiveScreen() and not(self.gettingCloserToCenterOfScreen()):
           self.warp()

    def gettingCloserToCenterOfScreen(self):
        #dot product of velocity vector and vector towards center
        #if positive, getting closer to center, if negative, getting farther from center

        #velocity vector
        vx = self.data["velocity"]["x"]
        vy = self.data["velocity"]["y"]
        #vector towards center a
        sx = self.data["position"]["x"]
        sy = self.data["position"]["y"]
        cx = SETUP.WIDTH/2
        cy = SETUP.HEIGHT/2

        ax = cx - sx
        ay = cy - sy

        #dot product vx * ax + vy *ay
        dotProduct = vx * ax + vy * ay
        return dotProduct > 0


        
    @classmethod
    def generateRandomStart(cls):
        #flip four sided dice, for which side the thing should start from
        minDistanceFromEdge = 500
        spawnableWidth = 1000
        sideSelector = random.randint(0, 3)
        if sideSelector == 0:
            #left side
            x = random.randint(-(minDistanceFromEdge + spawnableWidth), -minDistanceFromEdge)
            y = random.randint(-(minDistanceFromEdge + spawnableWidth), SETUP.HEIGHT + minDistanceFromEdge + spawnableWidth)
        if sideSelector == 1:
            #top
            x = random.randint(-(minDistanceFromEdge + spawnableWidth), SETUP.WIDTH + minDistanceFromEdge + spawnableWidth)
            y = random.randint(-(minDistanceFromEdge + spawnableWidth), -minDistanceFromEdge)
        if sideSelector == 2:
            #right side
            x = random.randint(SETUP.WIDTH + minDistanceFromEdge, SETUP.WIDTH + minDistanceFromEdge + spawnableWidth)
            y = random.randint(-(minDistanceFromEdge + spawnableWidth), SETUP.HEIGHT + minDistanceFromEdge + spawnableWidth)
        if sideSelector == 3:
            #bottom
            x = random.randint(-(minDistanceFromEdge + spawnableWidth), SETUP.WIDTH + minDistanceFromEdge + spawnableWidth)
            y = random.randint(SETUP.HEIGHT + minDistanceFromEdge, SETUP.HEIGHT + minDistanceFromEdge + spawnableWidth)
        return (x, y)

    def warp(self):
        self.data["canCollide"] = False
        #generate point of pass through 
        cx = random.randrange(50, SETUP.WIDTH - 50)
        cy = random.randrange(50, SETUP.HEIGHT - 50)

        sx, sy = Planet.generateRandomStart()

        self.data["position"]["x"] = sx 
        self.data["position"]["y"] = sy
        #this will find us a center location that does not collide with anything else
        while self.wouldBeCollidingSoon():
            #pick random starting location - only from the left and right for now 
            sx, sy = Planet.generateRandomStart()

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
        self.rect.centerx = self.data["position"]["x"]
        self.rect.centery = self.data["position"]["y"]
        surface.blit(self.image, self.rect)
        #pygame.draw.circle(surface, self.data["color"], (self.data["position"]["x"],self.data["position"]["y"]), self.data["radius"])

    @classmethod
    def generatePlanets(cls, count):
        #TODO: make this use the logic for warp and check if shit is gonna be colliding before making planets
        i = 0
        while i<count:
            xpos = random.randrange(0, SETUP.WIDTH)
            ypos = random.randrange(0, SETUP.HEIGHT)
            xvel = random.randrange(-SETUP.MAXSPEED, SETUP.MAXSPEED)
            yvel = random.randrange(-SETUP.MAXSPEED, SETUP.MAXSPEED)
            r = random.randrange(20, 100)
            Planet({"radius": r, "position": {"x": xpos, "y": ypos}, "velocity": {"x": xvel, "y": yvel}})
            i+=1
        
    @classmethod
    def generatePlanetsThatWillCollide(cls):
        #TODO: make this use the logic for warp and check if shit is gonna be colliding before making planets
        #random radii
        r1 = random.randrange(20, 100)
        r2 = random.randrange(20, 100)
        #generate point of collision 
        cx = random.randrange(50, SETUP.WIDTH - 50)
        cy = random.randrange(50, SETUP.HEIGHT - 50)
        #pick random starting locations - only from the left and right for now 
        sx1 = random.randint(-1000, 0)
        sx2 = random.randint(SETUP.WIDTH, SETUP.WIDTH+1000)

        sy1 = random.randint(-1000, SETUP.HEIGHT+1000)
        sy2 = random.randint(-1000, SETUP.HEIGHT+1000)
        
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
        
        
