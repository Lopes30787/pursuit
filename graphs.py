import my_pursuit.pursuit as pursuit_v4
from my_pursuit.utils2 import compare_results
import numpy as np
from policies import *
from multiprocess import Pool

EPISODES = 50


def do_policy(Policy):
    global rewards, steps

    env = pursuit_v4.env( max_cycles=200, x_size=16, y_size=16, shared_reward=True, n_evaders=30,
                         n_pursuers=8, obs_range=0, n_catch=2, freeze_evaders=False, tag_reward=0.05,
                         catch_reward=5.0, urgency_reward=-0.25, surround=True)
    
    reward = np.zeros(EPISODES)
    step = np.zeros(EPISODES)

    for i in range(EPISODES):
        env.reset()
        
        policy = Policy(env)

        for agent in env.agent_iter():
            observation, r, termination, truncation, info = env.last()

            if termination or truncation:
                action = None
            else:
                action = policy(observation, agent)
                step[i] += 1

            reward[i] += r

            env.step(action)

    return Policy.__name__, reward / 8, step / 8
    

policies = [RandomPolicy, GreedyPolicy, CoordinatedPolicy, RolePolicy, RolePolicy2, TotallyCoordinatedPolicy]


with Pool(len(policies)) as p:
    res = p.map(do_policy, policies)

rewards = {}
steps = {}

for name, r, s in res:
    rewards[name] = r
    steps[name] = s

compare_results(
    rewards,
    title="Teams Comparison on 'Pursuit' Environment",
    metric="Reward per Episode",
    colors=["orange", "green", "blue", "gray", "red", "purple"],
    filename="Fig1.png"
)

compare_results(
    steps,
    title="Teams Comparison on 'Pursuit' Environment",
    metric="Steps per Episode",
    colors=["orange", "green", "blue", "gray", "red", "purple"],
    filename="Fig2.png"
)