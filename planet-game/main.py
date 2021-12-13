import pygame
import math
from planet import Planet
import setup as SETUP

pygame.init()

timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, math.floor(1000/SETUP.FPS))
Planet.generatePlanets(3)
Planet.generatePlanetsThatWillCollide()

def draw_window():
    SETUP.WIN.fill(SETUP.WHITE)
    Planet.doCollisions()
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
                print("Quiting")
                run = False
            elif event.type == timer_event:
                draw_window()
            elif event.type == pygame.MOUSEBUTTONUP:
                Planet.generatePlanetsThatWillCollide()
    pygame.display.quit()
    pygame.quit()

main()


