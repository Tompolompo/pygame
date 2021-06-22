# imports
import pygame
import random
from spacejet.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE
import spacejet.objects as objects
import time
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
) 

pygame.init() # Initialize

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Events
ADDENEMY = pygame.USEREVENT + 1
#ADDPRICE = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMY, random.randint(250,500))
#pygame.time.set_timer(ADDPRICE, 5000)


# Instantiate player.
player = objects.Player()

# Create groups to hold enemy sprites and all sprites
enemies = pygame.sprite.Group()
#prices = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

price = objects.Price()
#prices.add(price)
all_sprites.add(price)

score = objects.Score()
all_sprites.add(score)

# Setup the clock for a decent framerate
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

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = objects.Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        
       # elif event.type == ADDPRICE:
            
        #    new_price = objects.Price()
          #  prices.add(new_price)
         #   all_sprites.add(new_price)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Update enemy position
    enemies.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False


    if pygame.sprite.collide_rect(player, price):
        score.update()
        price.update()


    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of X frames per second
    clock.tick(FRAMERATE)


time.sleep(1.5)