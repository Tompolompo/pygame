import pygame
import random
from pingpong.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE
import pingpong.objects as objects
import time
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
) 

pygame.init() # Initialize

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

player = objects.Player()
ball = objects.Ball()
score = objects.Score()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(ball)
all_sprites.add(score)



clock = pygame.time.Clock()

running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    dead = ball.update()
    if dead:
        player.kill()
        ball.kill()
        running = False

    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.collide_rect(player, ball):
        ball.pong() 
        score.update()
        
    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of X frames per second
    clock.tick(FRAMERATE)


time.sleep(0.5)