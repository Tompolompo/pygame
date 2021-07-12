#from RL.pptrain import human_instruction
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
    K_RIGHT
) 

class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.clock = pygame.time.Clock()

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
        self.rewards = []

    
    def initial_state(self):
        state = np.array([[
            float(self.player.rect.left),
            float(self.player.rect.right), 
            float(self.ball.rect.centerx), 
            float(self.ball.rect.centery), 
            float(self.ball.xspeed), 
            float(self.ball.yspeed)
        ]])

        return self.scale_state(state)
    
    def scale_state(self, state):
        state[0][0] /= SCREEN_WIDTH
        state[0][1] /= SCREEN_WIDTH
        state[0][2] /= SCREEN_WIDTH
        state[0][3] /= SCREEN_HEIGHT
        state[0][4] /= SCREEN_WIDTH
        state[0][5] /= SCREEN_HEIGHT
        return state

    def step_game(self, action=1, human_feedback=False):

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
        
        if human_feedback:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_RIGHT] == 1:
                action = 1
            else:
                action = 0

        # Update the player sprite based on user keypresses
        self.player.updateRL(action)
        dead = self.ball.update()

        reward=0
        if dead:
            self.player.kill()
            self.ball.kill()
            self.done = True
            reward = -100

        self.screen.fill((0, 0, 0))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        if pygame.sprite.collide_rect(self.player, self.ball):
            self.ball.pong() 
            self.score.update()
            self.player.update_racket()
            reward = 10
        else:
            if self.ball.rect.centerx > self.player.rect.left and self.ball.rect.centerx < self.player.rect.right:
                reward = 1
            
            # OBS: TEST NON SPARSE REWARDS
            
        self.rewards.append(reward)
            
        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of X frames per second
        #self.clock.tick(FRAMERATE)

        state = np.array([[
            float(self.player.rect.left),
            float(self.player.rect.right), 
            float(self.ball.rect.centerx), 
            float(self.ball.rect.centery), 
            float(self.ball.xspeed), 
            float(self.ball.yspeed)
        ]])

        #print(f"State : {self.scale_state(state)}")
        #print(f"Reward : {reward}")

        # if self.done:
        #     print(self.rewards)
        #     self.rewards = []

        if human_feedback:
            self.clock.tick(FRAMERATE)
            return self.scale_state(state), reward, self.done, action
        else:
            return self.scale_state(state), reward, self.done

    def playback(self, episode, framerate=FRAMERATE):
        # OBS UNSCALE DATA!!!

        self.reset()

        for state in episode:

            self.player.rect.centerx = state[0]
            self.ball.rect.centerx = state[1]
            self.ball.rect.centery = state[2]

            self.screen.fill((0, 0, 0))

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)
            
            pygame.display.flip()

            self.clock.tick(framerate)
