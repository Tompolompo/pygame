import pygame
import random
from balance.settings import  SCREEN_WIDTH, SCREEN_HEIGHT, POLE_HIGHT, RACKET_SPEED, RACKET_WIDTH_START, RACKET_WIDTH_MIN, RACKET_WIDTH_DECREASE
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
) 

FIGPATH = "pingpong/figs/"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.racket_width = RACKET_WIDTH_START
        self.surf = pygame.Surface((self.racket_width, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT,
            )
        )
        self.speed = RACKET_SPEED

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
    
    def updateRL(self, action):
        if action == 0: #left
            self.rect.move_ip(-self.speed, 0)
        elif action == 1: #right
            self.rect.move_ip(self.speed, 0)
        #else:


        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update_racket(self):
        x_pos = self.rect.centerx
        self.racket_width = self.racket_width*RACKET_WIDTH_DECREASE if self.racket_width > RACKET_WIDTH_MIN else RACKET_WIDTH_MIN
        self.surf = pygame.Surface((self.racket_width, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                x_pos,
                SCREEN_HEIGHT,
            )
        )

    

class Pole(pygame.sprite.Sprite):
    def __init__(self):
        super(Pole, self).__init__()
        self.surf = pygame.Surface((POLE_HIGHT, 10))
        self.surf.set_colorkey((0,0,0))
        self.surf.fill((255, 255, 255))
        self.image = self.surf.copy()
        self.image.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT/2,
            )
        )
        self.rot = 0
        self.rot_speed = 2

        self.new_image = pygame.transform.rotate(self.surf , self.rot) 
        

    def rotate(self):
        old_bottom = self.rect.midbottom 
        # defining angle of the rotation  
        self.rot = (self.rot + self.rot_speed) % 360  
        # rotating the orignal image  
        self.new_image = pygame.transform.rotate(self.surf , self.rot)  
        self.rect = self.new_image.get_rect()  
        # set the rotated rectangle to the old center  
        self.rect.midbottom = old_bottom
    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):

        self.rotate()

        return False




class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.myFont = pygame.font.Font(f"{FIGPATH}AtariClassic.ttf", 30)
        self.white = (255,255,255)
        self.score = 0
        ### pass a string to myFont.render
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=10, top=10)
        

    def update(self):
        self.score += 1
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=10, top=10)
