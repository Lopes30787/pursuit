import my_pursuit.pursuit as pursuit_v4
from policies import *
env = pursuit_v4.env(render_mode='human', n_pursuers=8,
                     n_evaders=30, surround=False)

env.reset()

policy = CoordinatedPolicy(env)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
    else:
        # this is where you would insert your policy
        action = policy(observation, agent)

    env.step(action)

env.close()
