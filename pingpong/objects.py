import pygame
import random
from pingpong.settings import  SCREEN_WIDTH, SCREEN_HEIGHT, BALL_YSPEED_INCREASE, BALL_YSPEED_MAX, BALL_YSPEED_START, RACKET_SPEED, RACKET_WIDTH_START, RACKET_WIDTH_MIN, RACKET_WIDTH_DECREASE
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
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH
        
    
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
        self.xspeed = random.randint(3,10)
        self.yspeed = BALL_YSPEED_START

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
        self.yspeed *= -BALL_YSPEED_INCREASE
        if self.yspeed > BALL_YSPEED_MAX:
            self.yspeed = BALL_YSPEED_MAX

        # if random.randint(0,1) == 0:
        #     self.xspeed += -1
        # else:
        #     self.xspeed += 1

        # if self.xspeed > 20:
        #     self.xspeed = 20
        # elif self.xspeed < -20:
        #     self.xspeed = -20


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
