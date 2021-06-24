from pingpong import pingpongRL
from RL import RLagent 
import pickle
import time
import numpy as np

init_time_start = time.time()
game = pingpongRL.Game()
game.reset()
agent = RLagent.Agent(action_space=np.array([0,1]))
print(f"init time = {time.time()-init_time_start: .2f}")


def train(agent, game, episodes=100):
    start_time = time.time()
    episode_time = 0

    for episode in range(episodes):
        episode_start_time = time.time()
        action_time = 0
        step_time = 0
        learn_time = 0

        game.reset()
        state = game.initial_state()
        state = state.reshape([1,5])

        i=0
        done=False
        
        while not done:

            action_start_time = time.time()
            action = agent.choose_action(state, agent.get_epsilon(i)) # choose action
            action_time += time.time() - action_start_time

            step_start_time = time.time()
            next_state, reward, done = game.step_game(action) # take action and observe state and reward
            step_time += time.time() - step_start_time

            next_state = next_state.reshape([1,5])
            agent.remember(state, action, reward, next_state, done) # record
            state = next_state
            i+=1

        
        agent.scores.append(game.score.score)
        mean_scores = np.mean(agent.scores)
        print(f"Epsiode={episode}, last score = {game.score.score}, mean score = {mean_scores}")
        
        if mean_scores > agent.win_ticks and episode > 100: # if average score is over win_ticks for past 100 rounds
            print(f"Solved in {episode-100} episodes :)")
            break
            
        if episode > episodes:
            print(f"Did not solve in {episodes} episodes :(")
                
        learn_start_time = time.time()      
        agent.learn_post_episode() # update model
        learn_time += time.time() - learn_start_time

        episode_time = time.time() - episode_start_time
        overhead_time = episode_time - action_time - step_time - learn_time
        print(f"\tEpisode time = {episode_time: .2f}, action time = {action_time: .2f}, step time = {step_time: .2f}, learn_time = {learn_time: .2f}, overhead = {overhead_time: .1f}")

    tot_time = time.time() - start_time  

    print(f"Total time = {tot_time: .2f}")          

train(agent, game, episodes=1)

#PATH = "C:/Users/tomas/Desktop/summer projects/game/RL/agents/"
PATH = "RL/agents/"
pickle.dump(agent.memory, open(f'{PATH}{time.strftime("%y%m%d_%H%M")}.p', 'wb'))