import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
) 


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("figs/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH/2,
                SCREEN_HEIGHT,
            )
        )
        self.speed = 10

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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("figs/missile.png").convert()
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
        self.width = 20
        self.surf = pygame.image.load("figs/Banana.png").convert()
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH-self.width),
                random.randint(int(SCREEN_HEIGHT/3), SCREEN_HEIGHT-self.height),
            )
        )
        


    def update(self):
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH-self.width),
                random.randint(int(SCREEN_HEIGHT/3), SCREEN_HEIGHT-self.height),
            )
        )

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self.myFont = pygame.font.SysFont("Times New Roman", 40)
        self.white = (255,255,255)
        self.score = 0
        ### pass a string to myFont.render
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=0, top=0)
        

    def update(self):
        self.score += 1
        self.surf = self.myFont.render(f"score: {self.score}", 1, self.white)
        self.rect = self.surf.get_rect(left=0, top=0)
