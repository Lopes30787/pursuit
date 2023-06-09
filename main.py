import my_pursuit.pursuit as pursuit_v4
from policies import *
import argparse

POLICIES = {
    "random": RandomPolicy,
    "greedy": GreedyPolicy,
    "social": SocialPolicy,
    "role": RolePolicy,
    "mixed": MixedPolicy
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Pursuit AASMA 23', description='AASMA Project 23')
    
    parser.add_argument("-p", "--policy", default="mixed")

    args = parser.parse_args()

    if args.policy.lower() not in POLICIES:
        print("Please provide a valid policy.")
        exit(1)

    env = pursuit_v4.env(render_mode='human', max_cycles=250, x_size=16, y_size=16, shared_reward=True, n_evaders=30,
                         n_pursuers=8, obs_range=0, n_catch=2, freeze_evaders=False, tag_reward=0.05,
                         catch_reward=5.0, urgency_reward=-0.25, surround=True)

    env.reset()

    policy = POLICIES[args.policy.lower()](env)

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
        else:
            action = policy(observation, agent)

        env.step(action)

    env.close()
