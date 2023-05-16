import gym
import highway_env
from DSL import *
import numpy as np
import copy
from Opt_BUS import ParameterFinder
import time
from PriorityQueue import PriorityQueue
import random
import json
import time
from datetime import date

class Function:

    def __init__(self, func, obs, acts, n_sample=400):
        self.observations = obs[:n_sample]
        self.actions = acts[:n_sample]
        self.synthesizer = BottomUpSearch()
        self.func = func

    def set_IDs(self):
        self.ids = {}
        self.vars_based_on_ids = {}
        process = []
        for l in self.func:
            process.append(l)
        i = 1
        vars = []
        while len(process) != 0:
            att = process.pop(0)
            att.set_ID(i)
            self.ids.update({str(i): att})
            self.vars_based_on_ids.update({str(i): copy.deepcopy(vars)}) # this is just based on the line not the right scope of each variabels
            i+=1
            if type(att) is Att_Ite:
                temp = []
                for l in att.true_case + att.false_case:
                    temp.append(l)
                process = temp + process
            if isinstance(att, Att_Var):
                vars.append(att.var)
        self.max_id = i-1

    def to_string(self):
        s = ""
        process = []
        for l in self.func:
            process.append(l)
        i = 1
        while len(process) != 0:
            att = process.pop(0)
            #print(att.toString())
            s += att.to_string()
            s += "\n"
        return s

    def modify_by_ID(self, id, program):
        before = None
        if id is None:
            self.func = []
            self.func.append(program)
            return
        att = self.ids[str(id)]
        if isinstance(att, (Att_Var)):
            before = copy.deepcopy(att.program)
            att.program = program
        elif isinstance(att, (Att_Ite)):
            before = copy.deepcopy(att.condition)
            att.condition = program

        return before

    def improve_function(self, performance, observation, action, n_episodes = 100, max_time = 300, qSize = 20, bound = 15, total_time=30000, start_time = 0.0, env_name = "LunarLander-v2", initial_interaction = 0, pre_collisions = 0, t_n_p = 0, ops = {}):
        pre_performance = performance
        pre_collisions = pre_collisions
        n_interactions = initial_interaction
        total_n_progs = t_n_p

        performance_history = []
        std_history = []
        ids_history = []
        times_history = []
        interactions_history = []
        numberOfPrograms_history = []
        collisions_history = []

        order_id = 0
        while time.time() - start_time < total_time:
            if order_id < self.max_id:
                order_id+=1
            elif order_id == self.max_id:
                order_id = 1

            vars = self.vars_based_on_ids[str(order_id)]
            att = self.ids[str(order_id)]
            modified_performance = pre_performance

            try:
                if type(att) is AssignAction:
                    current_action = att.value
                    modified_performance = pre_performance
                    modified_collision = pre_collisions
                    best_action = current_action
                    for act in action:
                        if act != current_action:
                            att.value = act
                            try:
                                action_performance, action_std, action_collisions, action_interactions = self.evaluate(n_episodes, env_name)
                                print(action_performance)
                                n_interactions+=action_interactions
                                if modified_performance < action_performance:
                                    best_action = act
                                    modified_performance = action_performance
                                    modified_std = action_std
                                    modified_collision = action_collisions

                                    times_history.append(time.time())
                                    performance_history.append(action_performance)
                                    ids_history.append(att.id)
                                    interactions_history.append(n_interactions)
                                    collisions_history.append(action_collisions)
                                    total_n_progs+=1
                                    numberOfPrograms_history.append(total_n_progs)

                                else:
                                    times_history.append(time.time())
                                    performance_history.append(pre_performance)
                                    ids_history.append(att.id)
                                    interactions_history.append(n_interactions)
                                    collisions_history.append(pre_collisions)
                                    total_n_progs += 1
                                    numberOfPrograms_history.append(total_n_progs)

                            except:
                                continue

                    if pre_performance > modified_performance:
                        att.value = current_action
                        print("original was better")
                    else:
                        att.value = best_action
                        pre_performance = modified_performance
                        pre_collisions = modified_collision
                else:
                    print("before starting synthesis")
                    print(att.to_string())
                    original_att = copy.deepcopy(att)

                    best_programs, best_rewards, total_n_progs, interactions, collisions, times, numberOfPrograms = self.synthesizer.synthesize(
                        att.size + bound, self, att,
                        ops[att.name()], ops["constants"], observation, action,
                        vars, self.observations, self.actions, PiRL=True, wait_time=max_time,
                        q_size=qSize, env_name=env_name, n_episodes=n_episodes, pre_collisions=pre_collisions,
                        pre_interactions=n_interactions, pre_performance=pre_performance, n_progs=total_n_progs)

                    times_history += times
                    performance_history += best_rewards
                    interactions_history += interactions
                    collisions_history += collisions
                    numberOfPrograms_history += numberOfPrograms
                    ids_history += [att.id] * len(times)

                    if best_programs[-1] != None:
                        if isinstance(att, (Att_Var)):
                            att.program = best_programs[-1]
                        elif isinstance(att, (Att_Ite)):
                            att.condition = best_programs[-1]

                    modified_performance = best_rewards[-1]
                    modified_collision = collisions[-1]
                    n_interactions = interactions[-1]

                    print(pre_performance)
                    print(modified_performance)

                    if pre_performance is None:
                        pre_performance = modified_performance
                    elif pre_performance >= modified_performance:
                        if isinstance(att, (Att_Var)):
                            att.program = original_att.program
                        elif isinstance(att, (Att_Ite)):
                            att.condition = original_att.condition
                    else:
                        pre_performance = modified_performance
                        pre_collisions = modified_collision

                    print(self.to_string())
            except:
                break
            self.to_string()
            break

        return performance_history, std_history, ids_history, times_history, interactions_history, collisions_history, numberOfPrograms_history

    def evaluate_att(self, n_episodes, id, p, env_name):
        self.modify_by_ID(id, p)
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
        average = []
        steps = []
        n_collision = 0
        for i_episode in range(n_episodes):
            env.seed(i_episode)
            ob = env.reset()
            reward = 0
            n_steps = 0
            while True:
                if env_name == "highway-fast-v0":
                    ob = ob.reshape((12,))
                namespace = {'s': ob}
                for l in self.func:
                    l.interpret(namespace)
                action = namespace['act']
                ob, r_t, done, info = env.step(action)
                n_steps+=1
                reward += r_t
                if done:
                    steps.append(n_steps)
                    if env_name == "highway-fast-v0" and n_steps!= env.config["duration"]:
                        n_collision+=1
                    break
            average.append(reward)

        return np.mean(average), np.std(average), n_collision, sum(steps)

    def evaluate(self, n_episodes, env_name = "LunarLander-v2"):
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
        average = []
        n_collision = 0
        steps = []
        for i_episode in range(n_episodes):
            env.seed(i_episode)
            ob = env.reset()
            reward = 0
            n_steps = 0
            while True:
                if env_name == "highway-fast-v0":
                    ob = ob.reshape((12,))
                namespace = {'s': ob}
                for l in self.func:
                    l.interpret(namespace)
                action = namespace['act']
                ob, r_t, done, info = env.step(action)
                n_steps += 1
                reward += r_t
                if done:
                    steps.append(n_steps)
                    if env_name == "highway-fast-v0" and n_steps != env.config["duration"]:
                        n_collision += 1
                    break
            average.append(reward)

        return np.mean(average), np.std(average), n_collision, sum(steps)

    def collect_trajectories(self, n_episodes, env_name = "LunarLander-v2", max_step = 2000):
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
        observations = []
        steps = 0
        for i_episode in range(n_episodes):
            ob = env.reset()
            while True:
                observations.append(ob)
                if env_name == "highway-fast-v0":
                    ob = ob.reshape((12,))
                namespace = {'s': ob}
                for l in self.func:
                    l.interpret(namespace)
                action = namespace['act']
                ob, r_t, done, info = env.step(action)
                steps+=1
                if steps == max_step:
                    break
                if done:
                    break
            if steps == max_step:
                break

        return observations, steps

    def get_action(self, id, p):
        self.modify_by_ID(id, p)
        actions = []
        for ob in self.observations:
            namespace = {'s': ob}
            for l in self.func:
                l.interpret(namespace)
            action = namespace['act']
            actions.append(action)
        return actions

    def score(self, id, p):
        p_actions = self.get_action(id, p)
        similarities = 0
        for i in range(len(self.actions)):
            if self.actions[i] == p_actions[i]:
                similarities += 1
        return similarities / float(len(self.actions))

class ProgramList():

    def __init__(self):
        self.plist = {}

    def insert(self, program):

        if program.get_size() not in self.plist:
            self.plist[program.get_size()] = {}

        if program.name() not in self.plist[program.get_size()]:
            self.plist[program.get_size()][program.name()] = []

        self.plist[program.get_size()][program.name()].append(program)

    def init_plist(self, constant_values, observation_values, action_values, variables):
        for i in observation_values:
            p = Observation(i)
            self.insert(p)

        for i in constant_values:
            p = Num(i)
            self.insert(p)

        for i in action_values:
            p = AssignAction(i)
            self.insert(p)

        for i in variables:
            p = Variable(i)
            self.insert(p)

    def get_programs(self, size):

        if size in self.plist:
            return self.plist[size]
        return {}


class BottomUpSearch():

    def init_env(self, inout):
        env = {}
        for v in self._variables:
            env[v] = inout[v]
        return env

    def has_equivalent(self, function, p, id):
        try:
            p_out = function.get_action(id, p)
        except:
            return True
        tuple_out = tuple(p_out)
        if tuple_out not in self.outputs:
            self.outputs.add(tuple_out)
            return False
        return True

    def grow(self, plist, closed_list, operations, size):
        new_programs = []
        for op in operations:
            for p in op.grow(plist, size):
                if p not in closed_list:
                    closed_list.append(p)
                    new_programs.append(p)
                    yield p

        for p in new_programs:
            plist.insert(p)

    def synthesize(self, bound, function, attribute, operations, constant_values, observation_values, action_values, variables, observations, actions, PiRL=False, wait_time = 300, q_size = 20, env_name = "LunarLander-v2", n_episodes = 100, pre_performance = 0, pre_interactions = 0, pre_collisions = 0, n_progs = 0):

        all_programs = PriorityQueue(q_size)
        parameter_finder = ParameterFinder(observations, actions, attribute.id, function)
        founded = []
        init_prog = None
        if type(attribute) is Att_Var:
            init_prog = attribute.program
        elif type(attribute) is Att_Ite:
            init_prog = attribute.condition
        if init_prog is not None:
            init_prog_copy = copy.deepcopy(init_prog)
            if PiRL:
                parameter_finder.optimize(init_prog_copy)
            s = function.score(attribute.id, init_prog_copy)
            all_programs.push((s, init_prog_copy))

        times = [time.time()]
        interactions = [pre_interactions]
        best_programs = [copy.deepcopy(init_prog)]
        best_rewards = [pre_performance]
        initial_interaction = pre_interactions
        collisions = [pre_collisions]
        numberOfPrograms = [n_progs]

        total_numberOfPrograms = n_progs


        start = time.time()
        accepted_condition_nodes = set([Lt.name(), Or.name(), Gt.name(), Observation.name(), And.name(), Equal.name(), NotEqual.name(), Variable.name(), Lt_Eq.name(), Gt_Eq.name()])

        while time.time() - start < wait_time:
            closed_list = []
            plist = ProgramList()
            plist.init_plist(constant_values, observation_values, action_values, variables)
            self.outputs = set()
            for current_size in range(1, bound + 1):
                if time.time() - start > wait_time:
                    break
                for p in self.grow(plist, closed_list, operations, current_size):
                    total_numberOfPrograms += 1
                    if time.time() - start > wait_time:
                        break
                    if type(attribute) is Att_Ite and p.name() not in accepted_condition_nodes:
                        continue
                    else:
                        p_copy = copy.deepcopy(p)

                        if PiRL:
                            parameter_finder.optimize(p_copy)
                        try:
                            s = function.score(attribute.id, p_copy)
                        except:
                            continue

                        all_programs.push((s, p_copy))
                        if (s, p_copy) in all_programs.heap:
                            try:
                                reward, _, c, n_interaction = function.evaluate(n_episodes, env_name)
                                initial_interaction+=n_interaction
                                if best_rewards[-1] <= reward:
                                    best_rewards.append(reward)
                                    times.append(time.time())
                                    interactions.append(initial_interaction)
                                    collisions.append(c)
                                    best_programs.append(copy.deepcopy(p_copy))
                                    numberOfPrograms.append(total_numberOfPrograms)
                                else:
                                    last_reward = best_rewards[-1]
                                    last_program = best_programs[-1]
                                    best_rewards.append(last_reward)
                                    best_programs.append(last_program)
                                    times.append(time.time())
                                    interactions.append(initial_interaction)
                                    last_c = collisions[-1]
                                    collisions.append(last_c)
                                    numberOfPrograms.append(total_numberOfPrograms)
                            except Exception as e:
                                print(e)

                        if total_numberOfPrograms % 1000 == 0:
                            print('AST Size: ', current_size, 'Programs: ', total_numberOfPrograms)

        return best_programs, best_rewards, total_numberOfPrograms, interactions, collisions, times, numberOfPrograms



