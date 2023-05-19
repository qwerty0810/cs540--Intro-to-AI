import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =  20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999


def default_Q_value():
    return 0

if __name__ == "__main__":

    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v1")
    env.seed(1)
    env.action_space.np_random.seed(1)


    # You will need to update the Q_table in your iteration
    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.
    episode_reward_record = deque(maxlen=100)

    for i in range(EPISODES):
        episode_reward = 0
        done = False
        obs = env.reset()

        ##########################################################
        # YOU DO NOT NEED TO CHANGE ANYTHING ABOVE THIS LINE
        # TODO: Replace the following with Q-Learning

        while (not done):

            random_probability = np.random.rand()
            current_action_values = np.array([Q_table[(obs, action)] for action in range(env.action_space.n)])
            best_action = np.argmax(current_action_values)
            selected_action = env.action_space.sample() if random_probability <= EPSILON else best_action
            next_state, reward, done, info = env.step(selected_action)
            next_action_values = np.array([Q_table[(next_state, action)] for action in range(env.action_space.n)])
            max_next_value = np.amax(next_action_values)
            updated_value = (1 - LEARNING_RATE) * Q_table[(obs, selected_action)] + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_value)
            Q_table[(obs, selected_action)] = updated_value
            obs = next_state
            episode_reward += reward

        EPSILON = EPSILON * EPSILON_DECAY

        # END of TODO
        # YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE
        ##########################################################

        # record the reward for this episode
        episode_reward_record.append(episode_reward) 

        
        if i%100 ==0 and i>0:
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    #### DO NOT MODIFY ######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    model_file.close()
    #########################