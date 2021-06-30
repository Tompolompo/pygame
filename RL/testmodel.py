from pingpong import pingpongRL
from RL import RLagent 
import pickle
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras

PATH_DATA = "RL/agents/"

init_time_start = time.time()
game = pingpongRL.Game()
game.reset()
agent = RLagent.Agent(action_space=np.array([0,1]), model=keras.models.load_model("RL/agents/agent_pp_210630_0939/model"))
state = game.initial_state()
done = False

while not done:
    action = agent.choose_action_greedy(state) # choose action
    state, reward, done = game.step_game(action) # take action and observe state and reward
