# imports
import pygame
import random
from spacejet.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE, TIMEOUT
import spacejet.objects as objects
import time
import numpy as np
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
    #ADDENEMY = pygame.USEREVENT + 1

    def __init__(self):
        pygame.init() 

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 

        #pygame.time.set_timer(self.ADDENEMY, random.randint(250,500))

        self.player = objects.Player()
        #self.enemies = pygame.sprite.Group()
        self.price = objects.Price()
        self.score = objects.Score()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.price)
        self.all_sprites.add(self.score)

        self.clock = pygame.time.Clock()

        self.running = True
        self.timeout = TIMEOUT
        self.rewards = []
    
    def reset(self):
         
        pygame.init()

        self.player = objects.Player()
        #self.enemies = pygame.sprite.Group()
        self.price = objects.Price()
        self.score = objects.Score()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.price)
        self.all_sprites.add(self.score)
        self.timeout = TIMEOUT

        self.done = False
    
    def scale_state(self, state):
        state[0][0] /= SCREEN_WIDTH
        state[0][1] /= SCREEN_HEIGHT
        state[0][2] /= SCREEN_WIDTH
        state[0][3] /= SCREEN_HEIGHT

        return state

    def initial_state(self):
        state = np.array([[
            self.player.rect.centerx,
            self.player.rect.centery,
            self.price.rect.centerx,
            self.price.rect.centery
        ]])

        return self.scale_state(state)
        
        
    def step_game(self, action):
        
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
            # elif event.type == self.ADDENEMY:
            #     # Create the new enemy and add it to sprite groups
            #     new_enemy = objects.Enemy()
            #     self.enemies.add(new_enemy)
            #     self.all_sprites.add(new_enemy)
            

        # Update the player sprite based on user keypresses
        self.player.updateRL(action)
        
        # Update enemy position
        #self.enemies.update()

        # Fill the screen with black
        self.screen.fill((0, 0, 0))

        # Draw all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        # if pygame.sprite.spritecollideany(self.player, self.enemies):
        #     # If so, then remove the player and stop the loop
        #     self.player.kill()
        #     self.score.kill()
        #     self.price.kill()
        #     self.done = True

        if pygame.sprite.collide_rect(self.player, self.price):
            self.score.update()
            self.price.update()
            reward = self.timeout/TIMEOUT * 10
            self.timeout = TIMEOUT
        else:
            self.timeout -= 1
            reward = 1/(np.abs(self.player.rect.centerx - self.price.rect.centerx)/SCREEN_WIDTH + np.abs(self.player.rect.centery - self.price.rect.centery)/SCREEN_HEIGHT)

        if self.timeout < 0:
            self.done = True
            self.player.kill()
            self.score.kill()
            self.price.kill()
            reward = 0

        # self.rewards.append(round(reward,2))
        # if self.done:
        #     print(self.rewards)
        #     self.rewards = []

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of X frames per second
        #self.clock.tick(FRAMERATE)

        state = np.array([[
            self.player.rect.centerx,
            self.player.rect.centery,
            self.price.rect.centerx,
            self.price.rect.centery
            ]])

        return self.scale_state(state), reward, self.done 


    # def start_game(self):
    #     # Main loop

    #     while self.running:
    #         # for loop through the event queue
    #         for event in pygame.event.get():
    #             # Check for KEYDOWN event
    #             if event.type == KEYDOWN:
    #                 # If the Esc key is pressed, then exit the main loop
    #                 if event.key == K_ESCAPE:
    #                     self.running = False
    #             # Check for QUIT event. If QUIT, then set running to false.
    #             elif event.type == QUIT:
    #                 self.running = False

    #             # Add a new enemy?
    #             # elif event.type == self.ADDENEMY:
    #             #     # Create the new enemy and add it to sprite groups
    #             #     new_enemy = objects.Enemy()
    #             #     self.enemies.add(new_enemy)
    #             #     self.all_sprites.add(new_enemy)
                

    #         # Get the set of keys pressed and check for user input
    #         pressed_keys = pygame.key.get_pressed()

    #         # Update the player sprite based on user keypresses
    #         self.player.update(pressed_keys)
            
    #         # Update enemy position
    #         self.enemies.update()

    #         # Fill the screen with black
    #         self.screen.fill((0, 0, 0))

    #         # Draw all sprites
    #         for entity in self.all_sprites:
    #             self.screen.blit(entity.surf, entity.rect)

    #         # Check if any enemies have collided with the player
    #         if pygame.sprite.spritecollideany(self.player, self.enemies):
    #             # If so, then remove the player and stop the loop
    #             self.player.kill()
    #             self.score.kill()
    #             self.price.kill()
    #             self.running = False

    #         if pygame.sprite.collide_rect(self.player, self.price):
    #             self.score.update()
    #             self.price.update()


    #         # Update the display
    #         pygame.display.flip()

    #         # Ensure program maintains a rate of X frames per second
    #         self.clock.tick(FRAMERATE)

    #     time.sleep(0.5)


