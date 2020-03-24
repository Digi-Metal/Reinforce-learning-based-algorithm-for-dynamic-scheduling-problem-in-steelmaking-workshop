#-*- coding:utf-8 -*-

"""
deep deterministic policy gradient test
"""

import os
import gym
import numpy as np

from DDPG import *

# 环境参数
env_name = 'MountainCarContinuous-v0'
env_seed = False
random_seed = 9527

# 创建gym游戏
env = gym.make(env_name).unwrapped
# 一般情况下不使用
if env_seed:
    env.seed(random_seed)
    torch.manual_seed(random_seed)
    np.random.seed(random_seed)

# 强化学习参数
state_dim = env.observation_space.shape[0]      # 状态个数
hidden_dim = 400
action_dim = env.action_space.n     # 动作个数

# 其它参数
num_episodes = 1000     # 训练时走几次
num_steps = 100     # 训练时一次走几步
test_iteration = 10     # 测试时走几次
num_test_steps = 200    # 测试时一次走几步
mode = 'train'      # train or test

retrain = True        # 是否重头训练
weight_num = 900        # 载入权重的代数,用于中途继续训练和test情况
log_interval = 100       # 每隔log_interval保存一次参数
print_log = 5       # 每走print_log次输出一次
