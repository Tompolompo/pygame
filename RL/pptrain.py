from pingpong import pingpongRL, objects
from RL import RLagent 
import pickle
import time
import numpy as np
import os
import tensorflow as tf

print('************* STARTING PPTRAIN ***************')
tf.debugging.set_log_device_placement(True)
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
c = tf.matmul(a, b)

print(c)

print("*********************************************")

PATH_DATA = "RL/agents/"

init_time_start = time.time()
game = pingpongRL.Game()
game.reset()
agent = RLagent.Agent(action_space=np.array([0,1]))
print(f"init time = {time.time()-init_time_start: .2f}")


def train(agent, game, episodes=100):
    start_time = time.time()
    episode_time = 0
    
    folder_name = f'RL/agents/agent_pp_{time.strftime("%y%m%d_%H%M")}'
    os.mkdir(folder_name)
    settings = {
        "episodes": episodes,
        "epsilon": agent.epsilon,
        "epsilon_step_decay": agent.epsilon_step_decay,
        "epsilon_episode_decay": agent.epsilon_episode_decay,
        "epsilon_min": agent.epsilon_min,
        "racket_speed": objects.RACKET_SPEED,
        "racket_width_start": objects.RACKET_WIDTH_START,
        "racket_width_min": objects.RACKET_WIDTH_MIN,
        "racket_width_decrease": objects.RACKET_WIDTH_DECREASE,
        "ball_yspeed_start": objects.BALL_YSPEED_START,
        "ball_yspeed_max": objects.BALL_YSPEED_MAX,
        "ball_yspeed_increase": objects.BALL_YSPEED_INCREASE
        }
    print(f"folder created: {folder_name}")
    pickle.dump(settings, open(f"{folder_name}/settings.p", 'wb'))


    for episode in range(episodes):
        episode_start_time = time.time()
        action_time = 0
        step_time = 0
        learn_time = 0

        game.reset()
        state = game.initial_state()
        state = state.reshape([1,6])

        i=0
        done=False
        while not done:

            action_start_time = time.time()
            if (i+1)%10 == 0:
                action = agent.choose_action_greedy(state)
            else:
                action = agent.choose_action(state, agent.get_epsilon(i)) # choose action
            action_time += time.time() - action_start_time

            step_start_time = time.time()
            next_state, reward, done = game.step_game(action) # take action and observe state and reward
            step_time += time.time() - step_start_time

            next_state = next_state.reshape([1,6])
            agent.remember(state, action, reward, next_state, done) # record
            state = next_state
            i+=1

        
        agent.scores.append(game.score.score)
        mean_scores = np.mean(agent.scores)
        print(f"Epsiode={episode}, last score = {game.score.score}, mean score = {mean_scores: .2f}")
        
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

        
        pickle.dump(agent.memory, open(f'{folder_name}/memory.p', 'wb'))
        pickle.dump(agent.loss_history, open(f'{folder_name}/loss.p', 'wb'))
        pickle.dump(agent.scores, open(f'{folder_name}/scores.p', 'wb'))
        agent.model.save(f'{folder_name}/model')


    tot_time = time.time() - start_time  

    print(f"Total time = {tot_time: .1f} seconds") 

def human_instruction(agent, game, episodes=1):

    for episode in range(episodes):

        game.reset()
        state = game.initial_state()
        state = state.reshape([1,6])

        i=0
        done=False
        while not done:
            next_state, reward, done, action = game.step_game(human_feedback=True) # take action and observe state and reward

            next_state = next_state.reshape([1,6])
            agent.remember(state, action, reward, next_state, done) # record
            state = next_state
            i+=1
        
        agent.learn_post_episode()



    return agent



# MAIN:
#agent = human_instruction(agent, game)
#with tf.device('/device:GPU:0'):
train(agent, game, episodes=1)

print("*************** end of pptrain *****************")
print("model:")
print(agent.model)
