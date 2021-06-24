import numpy as np
import pickle
from pingpong import pingpongRL

PATH = "RL/agents/"
mem = pickle.load(open(f"{PATH}{210623}_{1609}.p", "rb"))

episode = []
for m in mem:
    episode.append(m[0][0])
    if m[4]:
        break

game = pingpongRL.Game()
game.playback(episode)

