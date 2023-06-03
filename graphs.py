import my_pursuit.pursuit as pursuit_v4
from my_pursuit.utils2 import compare_results
import numpy as np
from policies import *

env = pursuit_v4.env(render_mode='human', n_pursuers=8,
                     n_evaders=30, surround=True)

env.reset()

policies = [RandomPolicy(env), GreedyPolicy(env), CoordinatedPolicy(env)]

results = []
rewards = []

for policy in policies:
    for i in range(5):
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
            else:
                # this is where you would insert your policy
                action = policy(observation, agent)

            env.step(action)
        rewards += [reward,]
        env.reset()
    results += [rewards,]
    rewards = []
    env.reset()

env.close()

print(results)
results_dict = { "Random Policy"      : np.array(results[0]),
                 "Greedy Policy"      : np.array(results[1]),
                 "Coordinated Policy" : np.array(results[2])}

compare_results(
    results_dict,
    title="Teams Comparison on 'Pursuit' Environment",
    metric="Reward per Episode",
    colors=["orange", "green", "blue", "gray"]
)