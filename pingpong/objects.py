import pygame
import random
from pingpong.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from pygame.locals import (
    RLEACCEL,
    K_LEFT,
    K_RIGHT,
) 

FIGPATH = "C:/Users/tomas/Desktop/summer projects/game/pingpong/figs/"

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((SCREEN_WIDTH/2, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT,
            )
        )
        self.speed = 10

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
        else: #right
            self.rect.move_ip(self.speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    




class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                10,
            )
        )
        self.xspeed = random.randint(-5,5)
        self.yspeed = 10

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        if self.rect.left < 0:
            self.xspeed *= -1
        if self.rect.right > SCREEN_WIDTH:
            self.xspeed *= -1
        if self.rect.top < 0:
            self.yspeed *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            return True

        self.rect.move_ip(self.xspeed, self.yspeed)
        return False

    def pong(self):
        self.yspeed *= -1.01
        if random.randint(0,1) == 0:
            self.xspeed += -1
        else:
            self.xspeed += 1

        if self.xspeed > 10:
            self.xspeed = 10
        elif self.xspeed < -10:
            self.xspeed = -10


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
