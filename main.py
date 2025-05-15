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


    # test 
    pygame.display.set_caption("Game Over Example")
    font = pygame.font.SysFont(None, 72)  # You can use a font name or None for default
    text = font.render("Game Over", True, (255, 0, 0))  # Red text
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Centered


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
    
    

    game_over = False




    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


        if game_over:
            # test
            screen.fill("black")
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            print("Game over!")
            return 



        # pygame.Surface.fill(screen,(0,0,0))
        updatable.update(dt)

        for obj in asteroids:
            for shoot in shots:
                if obj.check_collision(shoot):
                    shoot.kill()
                    obj.kill()
                    obj.split()

            if obj.check_collision(player):
                game_over = True
                #sys.exit()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000




if __name__ =="__main__" :
    main()
