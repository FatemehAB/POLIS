
import gym
import random
import torch
import numpy as np
from collections import deque
import matplotlib.pyplot as plt
from PriorityQueue import PriorityQueue
from DQN.State import State
import highway_env

def collecting_data(dir_folder, file_name, env_name, highlight, episodes = 120):

    env = gym.make(env_name)
    if env_name == "highway-fast-v0":
        env.config["lanes_count"] = 3
        env.config["policy_frequency"] = 1
        env.config['simulation_frequency'] = 15
        config = {
            "observation": {
                "type": "Kinematics",
                "vehicles_count": 3,
                "features": ["x", "y", "vx", "vy"],
                "absolute": True,
                "normalize": False
            },
            "disable_collision_checks": True,
            "duration": 50,
            'high_speed_reward': 0.4,
            'reward_speed_range': [15, 30],
            'right_lane_reward': 0.6,
            "other_vehicles_type": "highway_env.vehicle.behavior.AggressiveVehicle",
        }
        env.configure(config)
    print('State shape: ', env.observation_space.shape)
    print('Number of actions: ', env.action_space.n)

    from DQN.dqn_agent import Agent
    if env_name == "LunarLander-v2":
        agent = Agent(state_size=8, action_size=4, seed=None)
    elif env_name == "CartPole-v0":
        agent = Agent(state_size=4, action_size=2, seed=None)
    elif env_name == "Acrobot-v1":
        agent = Agent(state_size=6, action_size=3, seed=None)
    elif env_name == "highway-fast-v0":
        agent = Agent(state_size=12, action_size=5, seed=None)
    states = PriorityQueue(2000)
    #states_neg = PriorityQueue(200)
    observations_all = []
    actions_all =[]
    agent.qnetwork_local.load_state_dict(torch.load(dir_folder+file_name +'checkpoint_complete.pth'))
    a_r = []
    n_collision = 0
    n_steps = []
    total_steps = 0
    for i in range(episodes):
        state = env.reset()
        ret = 0
        steps = 0
        while True:
            if env_name == "highway-fast-v0":
                state = state.reshape((12,))
            action, q_val = agent.evaluate_q(state)
            observations_all.append(state)
            actions_all.append(action)
            I = max(q_val[0]) - min(q_val[0])
            s = State(state, action)
            states.push((I, s))
            state, reward, done, _ = env.step(action)
            steps+=1
            total_steps+=1
            ret += reward
            if not highlight and len(observations_all) == 400:
                break
            if highlight and len(states.heap) == 2000:
                break
            if done:
                a_r.append(ret)
                n_steps.append(steps)
                if steps != env.config["duration"]:
                    n_collision+=1
                break
        if not highlight and len(observations_all) == 400:
            break
        if highlight and len(states.heap) == 2000:
            break
    print(np.mean(a_r))
    print(np.std(a_r))
    print("steps: ")
    print(np.mean(n_steps))
    print("collisions: ")
    print(n_collision)
    print("interactions:")
    print(sum(n_steps))
    observations = []
    actions = []
    all_states = states.getAll()
    for s in all_states:
        observations.append(s[1].observation)
        actions.append(s[1].action)
    env.close()
    if highlight:
        return observations, actions, total_steps
    else:
        return observations_all, actions_all, total_steps
