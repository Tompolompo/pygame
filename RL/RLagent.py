#import os
#os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
import tensorflow as tf
from collections import deque
from tensorflow import keras
import random
import numpy as np
import math

class Agent(object):
    """The world's simplest agent!""" #0.99, 0.98
    def __init__(self, action_space, state_space=6, gamma=0.99, epsilon=1.0, epsilon_min=0.01, epsilon_step_decay=0.9925, epsilon_episode_decay=0.98, alpha=0.01, alpha_decay=0.01, batch_size=512, model=None):
        """ action =[left, right] """
        self.action_space = action_space # [left, right] left=0, right=1 {np.array([0,1])}
        self.memory = deque(maxlen=1000000) # saving history of episodes. used for training
        self.epsilon = epsilon # epsilon random
        self.epsilon_step_decay = epsilon_step_decay # decayrate for epsilon
        self.epsilon_episode_decay = epsilon_episode_decay # decayrate for epsilon
        self.epsilon_min = epsilon_min # decays to min value
        self.batch_size = batch_size # batch size used for training
        self.gamma = gamma # discount rate for reward
        self.win_ticks = 10 # av score to complete
        self.loss_history = deque(maxlen=1000)
        self.scores = deque(maxlen=1000)
        
        if model:
            self.model = model
        else:
            self.model = tf.keras.models.Sequential()
            self.model.add(tf.keras.layers.Dense(24, input_dim=state_space, activation='tanh')) # input the 5 dimensions of the state
            self.model.add(tf.keras.layers.Dense(48, activation='tanh'))
            self.model.add(tf.keras.layers.Dense(len(action_space), activation='linear')) # output the Q-values (value function) for the two actions

            optimizer=keras.optimizers.Adam(learning_rate=alpha, decay=alpha_decay)
            loss = keras.losses.MeanSquaredError()
            self.model.compile(optimizer=optimizer, loss=loss)

    def choose_action(self, state, epsilon):
        """ state = [racket x pos, ball x pos, ball y pos, ball x vel, ball y vel] """
        return np.random.choice(self.action_space) if (np.random.random() <= epsilon) else np.argmax(self.model.predict(state))

    def choose_action_greedy(self, state):
        return np.argmax(self.model.predict(state))

    def get_epsilon(self, t):
        return max(self.epsilon_min, self.epsilon * self.epsilon_step_decay ** t)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def learn_post_episode(self):
        #print(f"\tLearning post episode. memory = {len(self.memory)}")
        x_batch, y_batch = [], []
        minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))
        for state, action, reward, next_state, done in minibatch:
            y_target = self.model.predict(state) # q value for action 0 and 1
            y_target[0][action] = reward if done else self.gamma * np.max(self.model.predict(next_state)[0])
            x_batch.append(state[0])
            y_batch.append(y_target[0])
            
        # train model
        result = self.model.fit(np.array(x_batch), np.array(y_batch), len(x_batch), verbose=0)
        self.loss_history.append(result.history['loss'][0])
        #print(f"\tLoss = {result.history['loss'][0]}")
        # update epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_episode_decay