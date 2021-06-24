from pingpong import pingpongRL
from RL import RLagent 
import pickle
import time
import numpy as np

init_time_start = time.time()
game = pingpongRL.Game()
game.reset()
agent = RLagent.Agent(action_space=np.array([0,1]))
print(f"init time = {time.time()-init_time_start}")
#state = game.initial_state()


# step = 0
# done = False
# while not done:
#     print(f"step = {step}")
#     print(f"\t State = {state}")

#     action = agent.choose_action(state, agent.get_epsilon(step))
#     print(f"\t Action = {action}")

#     state, reward, done = game.step_game(action)

#     step += 1



def train(agent, game, episodes=100, visualize=True, show_every=10):
    #observation = [0,0,0,0,0]
    #reward = 1
    #success = 0
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
        #fig_data_temp = []
        i=0
        done=False
        
        while not done:
            #fig_data_temp.append(env.render(mode='rgb_array'))
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
                
        # if episode%show_every==0:
        #     fig_data.append(fig_data_temp)
        #     if visualize:
        #         show_video(fig_data[episode])
        
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
        print(f"Episode time = {episode_time}, action time = {action_time}, step time = {step_time}, learn_time = {learn_time}, overhead = {overhead_time}")

    tot_time = time.time() - start_time  

    print(f"Total time = {tot_time}")          

train(agent, game, episodes=500)

PATH = "C:/Users/tomas/Desktop/summer projects/game/RL/agents/"
pickle.dump(agent.memory, open(f'{PATH}{time.strftime("%y%m%d_%H%M")}.p', 'wb'))