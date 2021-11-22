import pygame
import math
from planet import Planet
import setup as SETUP

pygame.init()
pygame.font.init()

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, math.floor(1000/SETUP.FPS))
Planet.generatePlanets(4)

def draw_window():
    SETUP.WIN.fill(SETUP.WHITE)
    Planet.updatePositions()
    for planet in Planet.planets:
        planet.render(SETUP.WIN)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(SETUP.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("should quit")
                run = False
            elif event.type == timer_event:
                draw_window()
    pygame.display.quit()
    pygame.quit()

main()

