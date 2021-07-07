import pygame
import random
from spacejet.settings import SCREEN_WIDTH, SCREEN_HEIGHT

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
) 

FIGPATH = "C:/Users/tomas/Desktop/summer projects/game/spacejet/figs/"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.width = 50
        self.height = 50
        self.surf = pygame.image.load(f"{FIGPATH}jet.png").convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT,
            )
        )
        self.speed = 50

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def updateRL(self, action):
        if action == 0: #up
            self.rect.move_ip(0, -self.speed)
        if action == 1: #down
            self.rect.move_ip(0, self.speed)
        if action == 2: #left
            self.rect.move_ip(-self.speed, 0)
        if action == 3: #right
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    




class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(f"{FIGPATH}missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                0,
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()

class Price(pygame.sprite.Sprite):
    def __init__(self):
        super(Price, self).__init__()
        self.height = 50
        self.width = 50
        self.surf = pygame.image.load(f"{FIGPATH}banana.png").convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH-self.width),
                self.height,
            )
        )
        


    def update(self):
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH-self.width),
                random.randint(self.height, SCREEN_HEIGHT-self.height),
            )
        )

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.myFont = pygame.font.Font(f"{FIGPATH}AtariClassic.ttf", 20)
        self.white = (255,255,255)
        self.score = 0
        ### pass a string to myFont.render
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=10, top=10)
        

    def update(self):
        self.score += 1
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=10, top=10)
