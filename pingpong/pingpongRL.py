import pygame
import random
from pingpong.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FRAMERATE
import pingpong.objects as objects
import time
import numpy as np
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
) 

class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        #self.clock = pygame.time.Clock()

        # self.player = objects.Player()
        # self.ball = objects.Ball()
        # self.score = objects.Score()

        # self.all_sprites = pygame.sprite.Group()
        # self.all_sprites.add(self.player)
        # self.all_sprites.add(self.ball)
        # self.all_sprites.add(self.score)

        self.done = False
    
    def reset(self):
        pygame.init()

        self.player = objects.Player()
        self.ball = objects.Ball()
        self.score = objects.Score()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.score)

        self.done = False

    
    def initial_state(self):
        state = np.array([[
            self.player.rect.centerx, 
            self.ball.rect.centerx, 
            self.ball.rect.centery, 
            self.ball.xspeed, 
            self.ball.yspeed
        ]])

        return state

    def step_game(self, action):

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

        # Update the player sprite based on user keypresses
        self.player.updateRL(action)
        dead = self.ball.update()
        if dead:
            self.player.kill()
            self.ball.kill()
            self.done = True

        self.screen.fill((0, 0, 0))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        if pygame.sprite.collide_rect(self.player, self.ball):
            self.ball.pong() 
            self.score.update()
            reward = 1
        else:
            reward = 0
            
        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of X frames per second
        #self.clock.tick(FRAMERATE)

        state = np.array([[
            self.player.rect.centerx, 
            self.ball.rect.centerx, 
            self.ball.rect.centery, 
            self.ball.xspeed, 
            self.ball.yspeed
        ]])

        return state, reward, self.done
