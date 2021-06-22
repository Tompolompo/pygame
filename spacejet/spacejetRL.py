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
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
) 

class Game():

    # Events
    ADDENEMY = pygame.USEREVENT + 1

    def __init__(self):
        pygame.init() 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

        pygame.time.set_timer(self.ADDENEMY, random.randint(250,500))

        self.player = objects.Player()
        self.enemies = pygame.sprite.Group()
        self.price = objects.Price()
        self.score = objects.Score()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.price)
        self.all_sprites.add(self.score)

        self.clock = pygame.time.Clock()

        self.running = True
    
    def reinit(self):
         
        pygame.init()

        self.player = objects.Player()
        self.enemies = pygame.sprite.Group()
        self.price = objects.Price()
        self.score = objects.Score()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.price)
        self.all_sprites.add(self.score)

        self.running = True
        
        
    def step_game(self, actions):

        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    self.running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                self.running = False

            # Add a new enemy?
            elif event.type == self.ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = objects.Enemy()
                self.enemies.add(new_enemy)
                self.all_sprites.add(new_enemy)
            

        # Update the player sprite based on user keypresses
        self.player.updateRL(actions)
        
        # Update enemy position
        self.enemies.update()

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            # If so, then remove the player and stop the loop
            self.player.kill()
            self.score.kill()
            self.price.kill()
            self.running = False

        if pygame.sprite.collide_rect(self.player, self.price):
            self.score.update()
            self.price.update()


        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of X frames per second
        self.clock.tick(FRAMERATE)

        return self.score.score


    def start_game(self):
        # Main loop

        while self.running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.running = False

                # Add a new enemy?
                elif event.type == self.ADDENEMY:
                    # Create the new enemy and add it to sprite groups
                    new_enemy = objects.Enemy()
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)
                

            # Get the set of keys pressed and check for user input
            pressed_keys = pygame.key.get_pressed()

            # Update the player sprite based on user keypresses
            self.player.update(pressed_keys)
            
            # Update enemy position
            self.enemies.update()

            # Fill the screen with black
            self.screen.fill((0, 0, 0))

            # Draw all sprites
            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                # If so, then remove the player and stop the loop
                self.player.kill()
                self.score.kill()
                self.price.kill()
                self.running = False

            if pygame.sprite.collide_rect(self.player, self.price):
                self.score.update()
                self.price.update()


            # Update the display
            pygame.display.flip()

            # Ensure program maintains a rate of X frames per second
            self.clock.tick(FRAMERATE)

        time.sleep(0.5)


