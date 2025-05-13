import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shots import *


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH/2 ,SCREEN_HEIGHT/2)
    asteroidfield = AsteroidField()
    print("Starting Asteroids!")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # pygame.Surface.fill(screen,(0,0,0))
        updatable.update(dt)

        for obj in asteroids:
            if obj.check_collision(player):
                print("Game over!")
                sys.exit()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000




if __name__ =="__main__" :
    main()
