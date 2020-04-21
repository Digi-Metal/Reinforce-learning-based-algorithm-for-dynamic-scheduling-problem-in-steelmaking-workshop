#-*- coding:utf-8 -*-

"""
policy gradient test
"""

import os
import gym
import numpy as np

from PG import *

# 环境参数
env_name = 'CartPole-v0'
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

num_episodes = 1000     # 训练时走几次
num_steps = 100     # 训练时一次走几步
test_iteration = 10     # 测试时走几次
num_test_steps = 200    # 测试时一次走几步
mode = 'test'      # train or test
retrain = True        # 是否重头训练
weight_num = 900        # 载入权重的代数,用于中途继续训练和test情况
log_interval = 100       # 每隔log_interval保存一次参数
print_log = 5       # 每走print_log次输出一次

# use the cuda or not
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device == 'cuda':
    print('using the GPU...')
else:
    print('using the CPU...')

# 创建agent
agent = PolicyGradient(state_dim, hidden_dim, action_dim, device)

# create the directory to save the weight and the result
directory = './exp_pg_' + env_name +'./'
#directory = './exp_ddpg_' + env_name +'./'
if not os.path.exists(directory):    
    os.mkdir(directory)

if mode == 'train':
    # 是否中途开始训练
    if retrain == False:
        agent.load(directory, weight_num)
        
    # 训练; num_episodes:走多少次; i_episode:当前走到第几次; num_steps:每次走多少步 
    for i_episode in range(num_episodes):
        # 环境回归原位
        state = torch.Tensor([env.reset()])
        
        entropies = []
        log_probs = []
        rewards = []
        
        # 每次走num_steps步
        for t in range(num_steps):
            # 选action
            action, log_prob, entropy = agent.select_action(state)
            action = action.cpu()
            
            # 环境反馈
            # done:是否重新reset环境,大多游戏分为多个环节(episode),当done=true的时候,表示这个环节结束了
            next_state, reward, done, _ = env.step(action.numpy()[0])
            
            # 这些list记录了每次运行的每一步的数据, 如果需要, 可以提取数据得到训练过程的信息
            entropies.append(entropy)
            log_probs.append(log_prob)
            rewards.append(reward)
            
            # 更新state
            state = torch.Tensor([next_state])
            
            if done:
                break
            
        # 参数更新是每走一次更新一次, 不是每走一步更新一次
        agent.update(rewards, log_probs, entropies)
        
        # 保存权重并输出
        if i_episode % log_interval == 0 and i_episode != 0:
            agent.save(directory, i_episode)
        
        # 每隔几次输出一次信息
        if i_episode % print_log == 0 and i_episode != 0:
            # 输出回报
            print("Episode: {}, reward: {}".format(i_episode, np.sum(rewards)))
    env.close()
            
elif mode == 'test':
    # 载入权重
    agent.load(directory, weight_num)
    print("load weight...")
    
    for i_episode in range(test_iteration):
        state = torch.Tensor([env.reset()])
        for t in range(num_test_steps):
            # 选action
            action, log_prob, entropy = agent.select_action(state)
            action = action.cpu()
            
            # 环境反馈
            next_state, reward, done, _ = env.step(action.numpy()[0])
            # UI显示
            env.render()
            # 更新state
            state = torch.Tensor([next_state])
            if done:
                break
    env.close()
else:
    print("mode wrong!!!")
    
