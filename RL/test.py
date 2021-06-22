from pingpong import pingpongRL
from RL import RLagent 
import random
import numpy as np

action_space = np.array([0,1])
game = pingpongRL.Game()
game.reset()
agent = RLagent.Agent(action_space)

state = game.initial_state()
print(f"initial state = {state}")

step = 0
#while not done:
for i in range(5):
    print(f"step = {step}")
    print(f"\t State = {state}")

    action = agent.choose_action(state, agent.get_epsilon(i))
    print(f"\t Action = {action}")

    state, reward, done = game.step_game(action)

    step += 1


def train(agent, game, episodes=100, visualize=True, show_every=10):
    observation = [0,0,0,0,0]
    reward = 1
    success = 0
    

    for episode in range(episodes):
        game.reset()
        state = game.initial_state()
        state = state.reshape([1,4])
        #fig_data_temp = []
        i=0
        done=False
        
        while not done:
            #fig_data_temp.append(env.render(mode='rgb_array'))
            action = agent.choose_action(state, agent.get_epsilon(i)) # choose action
            next_state, reward, done = game.step(action) # take action and observe state and reward
            next_state = next_state.reshape([1,4])
            agent.remember(state, action, reward, next_state, done) # record
            state = next_state
            i+=1
        
        agent.scores.append(game.score.score)
        mean_scores = np.mean(agent.scores)
        print(f"Epsiode={episode}, last score = {i}, mean score = {mean_scores}")
                
        # if episode%show_every==0:
        #     fig_data.append(fig_data_temp)
        #     if visualize:
        #         show_video(fig_data[episode])
        
        if mean_scores > agent.win_ticks and episode > 100: # if average score is over win_ticks for past 100 rounds
            print(f"Solved in {episode-100} episodes :)")
            break
            
        if episode > episodes:
            print(f"Did not solve in {episodes} episodes :(")
                
                
        agent.learn_post_episode() # update model
                         
    