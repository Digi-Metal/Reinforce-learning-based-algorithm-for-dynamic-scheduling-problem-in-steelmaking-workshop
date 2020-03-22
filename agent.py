#-*- coding:utf-8 -*-

"""
agent
"""

import os
import gym
import numpy as np

from PG import *
from DDPG import *

# 环境参数
env_name = 'CartPole-v0'
env_seed = False
random_seed = 9527

# 强化学习参数
state_dim = env.observation_space.shape[0]      # 状态个数
hidden_dim = 400
action_dim = env.action_space.n     # 动作个数

num_episodes = 2000     # 训练时走几次
num_steps = 500     # 训练时一次走几步
mode = 'train'      # train or test
retrain = True        # 是否重头训练
weight_num = 100        # 如果不重头训练, 则为开始训练的代数
log_interval = 50       # 每隔log_interval保存一次参数
print_log = 5       # 每走print_log次输出一次

# use the cuda or not
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device == 'cuda':
    print('using the GPU...')

# 创建gym游戏
env = gym.make(env_name).unwrapped
# 一般情况下不使用
if env_seed:
    env.seed(random_seed)
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)

# 创建agent
agent = PolicyGradient(state_dim, hidden_dim, action_dim)

# the directory to save the weight and the result
directory = './exp_pg_' + args.env_name +'./'
directory = './exp_ddpg_' + args.env_name +'./'
if not os.path.exists(directory):    
    os.mkdir(directory)

if mode = 'train':
    # 是否中途开始训练
    if retrain = False:
        agent.load(weight_num)
        
    # 训练; num_episodes:走多少次; i_episode:当前走到第几次; num_steps:每次走多少步 
    for i_episode in range(num_episodes):
        # 环境回归原位
        state = torch.Tensor([env.reset()])
        
        entropies = []
        log_probs = []
        rewards = []
        
        # 每次走多少步
        for t in range(num_steps):
            # 选action
            action, log_prob, entropy = agent.select_action(state)
            action = action.cpu()

            # 环境反馈
            next_state, reward, done, _ = env.step(action.numpy()[0])
            
            # 这些list记录了每次运行的每一步的数据, 如果需要, 可以提取数据得到训练过程的信息
            entropies.append(entropy)
            log_probs.append(log_prob)
            rewards.append(reward)
            
            # 更新state
            state = torch.Tensor([next_state])
            
        # 参数更新是每走一次更新一次, 不是每走一步更新一次
        agent.update_parameters(rewards, log_probs, entropies)

        # 保存权重并输出
        if i_episode % log_interval == 0:
            torch.save(agent.model.state_dict(), os.path.join(dir, 'reinforce-'+str(i_episode)+'.pkl'))
        
        # 每隔几次输出一次信息
        if i_episode % print_log == 0:
            print("Episode: {}, reward: {}".format(i_episode, np.sum(rewards)))

env.close()
