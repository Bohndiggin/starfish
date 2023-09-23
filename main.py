import pygame
from utils import *

pygame.init()
screen = pygame.display.set_mode((pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]), flags=pygame.SCALED)
clock = pygame.time.Clock()
running = True
dt = 0

star1 = Star(screen=screen, temperature=5700, mass=1)
# planet1 = Planet(screen, star1)
# planet2 = Planet(screen, star1)
planet_list = []

def add_planets(num):
    planet_list.append(Planet(screen, star1))

add_planets(1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    star1.draw()
    for i in planet_list:
        i.update_location()

    if len(planet_list) < 600:
        add_planets(1)
    # add_planets(1)
    # print(len(planet_list), "planets")
    # print(int(clock.get_fps()))

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(144) / 1000  # limits FPS to 60

pygame.quit()