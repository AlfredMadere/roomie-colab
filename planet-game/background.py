import pygame
import setup as SETUP
class Background(pygame.sprite.Sprite):
    def __init__(self, imageFile, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(imageFile), (SETUP.WIDTH, SETUP.HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location