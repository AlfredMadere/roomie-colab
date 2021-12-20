from planet import Planet
import math 
import pygame
import random

class Player(pygame.sprite.Sprite):
    #The player will be able to travel circumfrentially around planets using the arrow keys and jump radially between them using the up arrow
    #this may cause issues with transparency
    avatar = pygame.image.load("./planet-game/assets/space sam alien.png").convert_alpha()
    def __init__(self, theta):
        pygame.sprite.Sprite.__init__(self)
        self.w = 70
        self.h = 70
        self.jumpSpeed = 1
        self.circumfrentialSpeed = 2
        self.lVelocity = pygame.Vector2(0,0)
        self.cVelocity = 0
        self.image = pygame.Surface([self.w, self.h])
        self.collisionRadius = max(self.w, self.h)
        self.theta = 0 #random.randint(0, 360)
        self.image = pygame.transform.scale(Player.avatar, (self.w, self.h))
        self.planet = Planet.planets[0]
        self.pos = self.planet.pos + pygame.Vector2(pygame.Vector2(self.planet.data["radius"] + self.h/2, 0), self.theta)
        self.jumping = False

        
    def render (self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.theta - 90)
        rotated_image_rect = rotated_image.get_rect(center = self.pos)
        pygame.draw.circle(surface, (0,0,0), self.pos, self.collisionRadius)
        surface.blit(rotated_image, rotated_image_rect)

    def moveCircumfrentially (self):
        self.theta += self.cVelocity
        self.pos = self.planet.pos + pygame.Vector2.rotate(pygame.Vector2(self.planet.data["radius"] + self.h/2, 0), -self.theta)

    def moveLinearly(self):
        self.theta += self.cVelocity
        self.pos.xy = (self.pos + self.lVelocity).xy

    def collides(self, planet):
        if pygame.Vector2.length_squared(pygame.Vector2(self.pos) - pygame.Vector2(planet.pos)) < self.collisionRadius**2+planet.data["radius"]**2:
            planet.data["color"] = (0, 255, 0)
            return True

    def handleLanding(self):
        #loop through planets to see if you are colliding with any of them, if you are, assign your planet to be the one you're colliding with
        #this is an issue if the radius of the collision circle makes it extend into the planet it's jumping off of
        #in this case it shouldn't ever really leave a planet... but for some reason it is
        print(str(Planet.planets))
        for planet in Planet.planets:
            print("planet" + str(planet))
            if self.collides(planet):
                self.planet = planet
                self.theta = ((math.atan((planet.pos.x - self.pos.x)/( planet.pos.y - self.pos.y))*180)/math.pi) - 90
                self.jumping = False
                print("jumping? " + str(self.jumping))

    def doAll (self, surface):
        self.handleControls()
        if self.jumping:
            self.moveLinearly()
            self.handleLanding()
        else:
            self.moveCircumfrentially()
            #self.handleCollisions()
        self.render(surface)

    def handleControls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not(self.jumping):
            self.lVelocity = self.jumpVelocity()
            self.jumping = True
            self.planet = None
        else:
            self.cVelocity = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.circumfrentialSpeed

        print("jumping? " + str(self.jumping))

    def jumpVelocity(self):
        #vector from center of planet to player
        v = self.pos - self.planet.pos
        pygame.math.Vector2.scale_to_length(v, self.jumpSpeed)
        return v

