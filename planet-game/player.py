from planet import Planet
import math 
import pygame

class Player(pygame.sprite.Sprite):
    #The player will be able to travel circumfrentially around planets using the arrow keys and jump radially between them using the up arrow
    #this may cause issues with transparency
    avatar = pygame.image.load("./planet-game/assets/space sam alien.png").convert_alpha()
    def __init__(self, theta):
        pygame.sprite.Sprite.__init__(self)
        w = 70
        h = 70
        self.jumpSpeed = 4
        self.circumfrentialSpeed = 2
        self.cVelocity = 0
        self.image = pygame.Surface([w, h])
        self.collisionRadius = min(w, h)
        self.theta = theta
        self.image = pygame.transform.scale(Player.avatar, (w, h))
        self.rect = self.image.get_rect()
        self.planet = Planet.planets[0]
        self.x = self.planet.data["position"]["x"] + self.planet.data["radius"]*math.cos(math.radians(self.theta))
        self.y = self.planet.data["position"]["y"] - self.planet.data["radius"]*math.sin(math.radians(self.theta))
        self.pos = pygame.Vector2(self.x, self.y)
        self.rect.center = (self.x, self.y)
        self.jumping = False
        
    def render (self, surface):
        self.x = self.planet.data["position"]["x"] + self.planet.data["radius"]*math.cos(math.radians(self.theta))
        self.y = self.planet.data["position"]["y"] - self.planet.data["radius"]*math.sin(math.radians(self.theta))
        #just render at x and y
        #So this will not work
        #I need to have access to the x and y corrdinates of the avatar becuase I only ever render it like this when it's actively on a planet
        #When the guy is moving though the air while jumping I need him to maintain his same orientation
        blitRotate(surface, self.image, (self.planet.data["position"]["x"], self.planet.data["position"]["y"]), (0, self.planet.data["radius"]), self.theta)

    def moveCircumfrentially (self):
        self.theta += self.cVelocity

    def moveLinearly(self):
        self.pos = self.pos + self.lVelocity

    def collides(self, planet):
        if (self.pos - planet.pos).length_squared() < self.collisionRadius**2+planet.data["radius"]**2:
            return True

    def handleLanding(self):
        #loop through planets to see if you are colliding with any of them, if you are, assign your planet to be the one you're colliding with
        for planet in Planet.planets:
            if self.collides(planet):
                self.planet = planet
                self.theta = math.atan(planet.data["position"]["x"] - self.pos[0]/ planet.data["position"]["y"] - self.pos[1])
                self.jumping = False

    def doAll (self):
        self.handleControls()
        if self.jumping:
            self.moveLinearly()
            self.handleLanding()
        else:
            self.moveCircumfrentially()
            #self.handleCollisions()
        self.render()

    def handleControls(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not(self.jumping):
            self.jumping = True
            self.planet = None
            self.lVelocity = self.jumpVelocity()
        else:
            self.cVelocity = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.circumfrentialSpeed

    def jumpVelocity(self):
        planetCenter = pygame.Vector2(self.planet.data["position"]["x"], self.planet.data["position"]["x"])
        selfCenter = pygame.Vector2(self.x, self.y)
        jumpVelocity = (selfCenter - planetCenter).scale_to_length(self.jumpSpeed)
        return jumpVelocity


def blitRotate(surf, image, origin, pivot, angle):
    #NEED TO FIGURE THIS SHIT OUT
    # offset from pivot to center
    image_rect = image.get_rect(midbottom = (origin[0] - pivot[0], origin[1] - pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)