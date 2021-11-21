import pygame
#from pygame.constants import HIDDEN

WIDTH, HEIGHT = 900, 500
WIN =  pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 0, 0)

def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        WIN.fill(WHITE)
        pygame.display.update()
    pygame.quit()

#if __name__ == "__index__":
main()


#pygame.draw.rect(pygame.Surface,pygame.Color.aliceblue,(395,0,10,10))