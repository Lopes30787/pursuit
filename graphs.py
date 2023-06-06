import my_pursuit.pursuit as pursuit_v4
from my_pursuit.utils2 import compare_results
import numpy as np
from policies import *

env = pursuit_v4.env( max_cycles=500, x_size=16, y_size=16, shared_reward=True, n_evaders=30,
                     n_pursuers=8,obs_range=0, n_catch=2, freeze_evaders=False, tag_reward=0.01,
                     catch_reward=5.0, urgency_reward=-0.1, surround=True)

env.reset()

policies = [RandomPolicy(env), GreedyPolicy(env), CoordinatedPolicy(env), RolePolicy(env), RolePolicy2(env)]

results = []
rewards = []
steps = []
step = 0
reward2 = [0,0,0,0,0,0,0,0]

for policy in policies:
    for i in range(5):
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            reward2.pop(0)
            reward2.append(reward)
            if termination or truncation:
                action = None
            else:
                # this is where you would insert your policy
                action = policy(observation, agent)

            env.step(action)
            step += 1
        rewards += [sum(reward2),]
        steps += [step/8,]
        step = 0
        reward2 = [0,0,0,0,0,0,0,0]
        env.reset()
    results += [rewards,]
    results += [steps,]
    rewards = []
    steps = []
    env.reset()

env.close()

print(results)
results_dict = { "Random Policy"      : np.array(results[0]),
                 "Greedy Policy"      : np.array(results[2]),
                 "Coordinated Policy" : np.array(results[4]),
                 "Role Policy"        : np.array(results[6]),
                 "Role Policy2"       : np.array(results[8])}

compare_results(
    results_dict,
    title="Teams Comparison on 'Pursuit' Environment",
    metric="Reward per Episode",
    colors=["orange", "green", "blue", "gray"]
)

results_dict = { "Random Policy"      : np.array(results[1]),
                 "Greedy Policy"      : np.array(results[3]),
                 "Coordinated Policy" : np.array(results[5]),
                 "Role Policy"        : np.array(results[7]),
                 "Role Policy2"       : np.array(results[9])}

compare_results(
    results_dict,
    title="Teams Comparison on 'Pursuit' Environment",
    metric="Steps per Episode",
    colors=["orange", "green", "blue", "gray", "red"]
)