import time
import gym
import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from DQN.evaluation import collecting_data
from DQN.dqn_agent import Agent

def dqn(n_episodes=2000, max_t=1000, eps_start=1.0, eps_end=0.01, eps_decay=0.995, file_name = ""):
    """Deep Q-Learning.
    
    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    env = gym.make('LunarLander-v2')
    # env.seed(0)
    print('State shape: ', env.observation_space.shape)
    print('Number of actions: ', env.action_space.n)
    agent = Agent(state_size=8, action_size=4, seed=None)
    scores = []                        # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start                    # initialize epsilon
    steps = 0
    times = [time.time()]
    torch.save(agent.qnetwork_local.state_dict(), 'checkpoints/' + file_name + str(0) + '.pth')
    for i_episode in range(1, n_episodes+1):
        state = env.reset()
        score = 0
        done = False
        while not done:
            action, _ = agent.act(state, eps)
            next_state, reward, done, _ = env.step(action)
            steps+=1
            agent.step(state, action, reward, next_state, done)
            state = next_state
            score += reward
            if done:
                break 
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score
        eps = max(eps_end, eps_decay*eps) # decrease epsilon
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), '\tsteps: {:.2f}'.format(steps), end="")
        if i_episode % 100 == 0:
            times.append(time.time())
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), '\tsteps: {:.2f}'.format(steps))
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoints/'+ file_name + str(i_episode) +'.pth')
        if np.mean(scores_window)>=200.0:
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(i_episode-100, np.mean(scores_window)), '\tsteps: {:.2f}'.format(steps))
        torch.save(agent.qnetwork_local.state_dict(), file_name + 'checkpoint_complete.pth')
            #break
    return scores, times
if __name__ == '__main__':

    #from eval import *
    for i in range(10):
        scores, times = dqn(file_name=str(i))
        np.save(str(i) + "times_models.npy", times)
        plt.plot(np.arange(len(scores)), scores)
        plt.ylabel('Score')
        plt.xlabel('Episode #')
        plt.savefig(str(i) + 'learning_curve_2000.png')
        plt.show()
        #env.close()
