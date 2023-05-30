# from pettingzoo.sisl import pursuit_v4
import my_pursuit.pursuit as pursuit_v4
from policies import Policies
env = pursuit_v4.env(render_mode='human', obs_range=7)

env.reset()

policy = Policies["RandomPolicy"](env)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        action = None
    else:
        # this is where you would insert your policy
        action = policy(observation, agent)

    env.step(action)
    break

pause()
env.close()
