from planet import Planet 
import pygame

class Player(pygame.sprite.Sprite):
    #The player will be able to travel circumfrentially around planets using the arrow keys and jump radially between them using the up arrow
    def __init__(self, planet, theta, avatar):
        super().__init__(self)
        w = 200
        h = 200
        self.image = pygame.Surface([w, h])
        self.planet = planet
        self.theta = theta
        self.avatar = avatar
        self.planet = Planet.planets[0]
        
    def render (self):
        #render player on its planets radius
        pass

    def updatePosition (self):
        #update posiiton by velocity, around circle
        pass
    
    