# GENERAL SETTINGS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FRAMERATE = 30 # only relevant for display (not for RL agent)

# RACKET SETTINGS
RACKET_SPEED = SCREEN_WIDTH/40
RACKET_WIDTH_START = SCREEN_WIDTH*0.5
RACKET_WIDTH_MIN = RACKET_SPEED
RACKET_WIDTH_DECREASE = 1.0

# BALL SETTINGS
BALL_YSPEED_START = SCREEN_HEIGHT/60
BALL_YSPEED_MAX = SCREEN_HEIGHT/2
BALL_YSPEED_INCREASE = 1.05
