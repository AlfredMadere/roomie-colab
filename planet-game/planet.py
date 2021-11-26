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
        Planet.planets.append(self)
   
    @classmethod
    def doCollisions(cls):
       for i, planet in enumerate(Planet.planets):
           if i != len(Planet.planets) - 1:
               for otherPlanet in Planet.planets[i+1:]:
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
        instantaniousDrag = self.drag()
        self.data["velocity"]["x"] *= (1.0 - instantaniousDrag)
        self.data["velocity"]["y"] *= (1.0 - instantaniousDrag)
        self.handleOutOfScreen()
            
         
    def warp(self):
        
        #random slope
        a = random.randint(-999,999)
        #random position point in middle half of canvas
        finalPosX = random.randint(0.25*SETUP.WIDTH, 0.75*SETUP.WIDTH)
        finalPosY = random.randint(0.25*SETUP.HEIGHT, 0.75*SETUP.HEIGHT)
        b = a*finalPosX + finalPosY
        
        #y-intercept of left x bound
        y1 = -1*(a*-100 + b)
        #y-intercept of right x bound
        y2 = -1*(a*1000 + b)
        #x-intercept of upper y bound
        if a == 0:
            x1 = -900
            x2 = -900
        else:
            x1 = (100 - b)/a
        #x-intercept of lower y bound
            x2 = (-600 - b)/a

        #check to see which of the intercepts found above lie on the box 100px from the screen
        #lines will often have intercepts on both x or y bounds, so In a random order I
        #checked each bound on the outer box and if the conditionals were true I updated
        #the postition and velocity of the planet so it should re-enter the canvas
       
            if(y1 >= 100 and y1<= 600):
                self.data["position"]["x"] = -100
                self.data["position"]["y"] = y1
                self.data["velocity"]["x"] = random.randint(2,5)*math.cos(1/a)
                self.data["velocity"]["y"] = random.randint(2,5)*math.sin(1/a) 
            elif(y2 >= 100 and y2<= 600):
                self.data["position"]["x"] = 1000
                self.data["position"]["y"] = y2
                self.data["velocity"]["x"] = random.randint(2,5)*math.cos(1/a)
                self.data["velocity"]["y"] = random.randint(2,5)*math.sin(1/a) 
            elif(x1 >= -100 and x1 <= 1000):
                self.data["position"]["x"] = x1
                self.data["position"]["y"] = -100
                self.data["velocity"]["x"] = random.randint(2,5)*math.cos(1/a)
                self.data["velocity"]["y"] = random.randint(2,5)*math.sin(1/a) 
            elif(x2 >= -100 and x2 <= 1000):
                self.data["position"]["x"] = x2
                self.data["position"]["y"] = 600
                self.data["velocity"]["x"] = random.randint(2,5)*math.cos(1/a)
                self.data["velocity"]["y"] = random.randint(2,5)*math.sin(1/a) 

    #Check if any planet fully leaves the screen
    #If planet leaves screen, call warp function
    #Loop through and check if planet collides with any other planet when it warped
    #While collission = true, continue warping the planet until it finds an open spot
    def handleOutOfScreen(self):
       for i in Planet.planets:
            posX = self.data["position"]["x"]
            posY = self.data["position"]["y"]
            rad = self.data["radius"]
            if posX < (-201) or posX > (1101) or posY < (-201) or posY > (701):
                self.warp()
                #for j in Planet.planets:
                 #   if j == i:
                  #      continue
                   # other = Planet.planets[j]
                    #while(Planet.collides(other)):
                     #   Planet.planets[i].warp()

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
        #generate point of collision - center for now
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

        Planet({"radius": r1, "position": {"x": sx1, "y": sy1}, "velocity": {"x": xvel1, "y": yvel1}})
        Planet({"radius": r2, "position": {"x": sx2, "y": sy2}, "velocity": {"x": xvel2, "y": yvel2}})

    @classmethod
    def updatePositions(cls):
        for planet in Planet.planets:
            planet.updatePosition()
        
        

