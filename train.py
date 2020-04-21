#-*- coding:utf-8 -*-

"""
训练神经网络
"""

import os
from ui import *
from utils import *
from environment import *

# use the cuda or not
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device == 'cuda':
    print('using the GPU...')
else:
    print('using the CPU...')

# create the directory to save the weight
directory = './weights./'
if not os.path.exists(directory):
    os.mkdir(directory)

# 新建agent
agent0 = InitialAgent(0, 4, 3, 0, 0.1, 5000, device)
agent1 = ProcessAgent(1, 6, 4, 0, 0.1, 50000, device)
agent2 = ProcessAgent(2, 5, 6, 0, 0.1, 50000, device)
agent3 = ProcessAgent(3, 3, 5, 0, 0.1, 5000, device)
agent4 = ProcessAgent(4, 4, 3, 0, 0.1, 5000, device)
agent5 = LastAgent(5, 2, 4, 5, 0, 0.1, 5000, device)
agent6 = LastAgent(5, 3, 4, 3, 0, 0.1, 5000, device)
agent7 = LastAgent(5, 4, 4, 4, 0, 0.1, 5000, device)

processAgents = [agent1, agent2, agent3, agent4]
lastAgents = [agent5, agent6, agent7]
agentsLs = [agent0, agent1, agent2, agent3, agent4, agent5, agent6, agent7]
agentsName = ['agent0', 'agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'agent6', 'agent7']


# 参数
num_episodes = 100000     # 训练多少次
retrain = True        # 是否重头训练
weight_num = 900        # 载入权重的代数,用于中途继续训练
log_interval = 100       # 每隔log_interval保存一次参数
print_log = 5       # 每走print_log次输出一次

env = Env() # 新建环境
# 是否中途开始训练
if retrain == False:
    for each in agentsLs:
        each.rl.load(directory, str(each), weight_num)

# 训练
for i_episode in range(num_episodes):
    env.reset() # 环境重置
    rewards = []
    
    # 每次训练
    while True:
        init_flag = 0
        env.count += 1
        
        # ===========InitialAgent操作===========
        state = toInitialAgentState(env) # 环境state转换成agent的state
        action = agent0.rl.select_action(state) # 选择动作
        action = agent0.rl.add_action_noise(action) # add noise to action
        
        # 环境反馈
        states, done = env.initialStep(agent0, action)
        next_state = toInitialAgentState(env)
        reward = -1
        
        # 如果决策出错
        if done:
            init_flag = 1
            reward = -10000
            #print("Decision failure, task failure")
            
        # 数据添加入replay_buffer
        agent0.rl.replay_buffer.push((state, next_state, action, reward, np.float(done)))
        rewards.append(reward) # 记录各步骤reward
        env.envStates = states # 更新states
        
        if init_flag == 1:
            break
        # ===========processAgent依次操作===========
        flag = 0
        for eachAgent in processAgents:
            process_flag = 0
            state = toProcessAgentState(env, eachAgent)
            action = eachAgent.rl.select_action(state)
            action = eachAgent.rl.add_action_noise(action)
            
            states, done = env.processStep(eachAgent, action)
            next_state = toProcessAgentState(env, eachAgent)
            reward = -1
            
            if done:
                process_flag = 1
                flag = 1
                reward = -100000
                #print("Decision failure, task failure")
            
            eachAgent.rl.replay_buffer.push((state, next_state, action, reward, np.float(done)))
            rewards.append(reward)
            env.envStates = states
            
            if process_flag == 1:
                break
        if flag == 1:
            break
            
        # ===========lastAgent依次操作===========
        flag = 0
        for eachAgent in lastAgents:
            last_flag = 0
            state = toLastAgentState(env, eachAgent)
            action = eachAgent.rl.select_action(state)
            action = eachAgent.rl.add_action_noise(action)
            
            states, done = env.lastStep(eachAgent, action)
            next_state = toLastAgentState(env, eachAgent)
            reward = -1
            
            if done:
                last_flag = 1
                flag = 1
                reward = -100000
                #print("Decision failure, task failure")
            
            eachAgent.rl.replay_buffer.push((state, next_state, action, reward, np.float(done)))
            rewards.append(reward)
            env.envStates = states
            
            if last_flag == 1:
                break
        if flag == 1:
            break
        
        # 调度系统正常完成
        if env.ifTaskFinish() == 1:
            print("Decision succeed")
            break
            
    # ===========其它操作===========
    # update
    for each in agentsLs:
        if len(each.rl.replay_buffer.storage) >= each.capacity-1:
            each.rl.update()
            
    # save
    if i_episode % log_interval == 0 and i_episode != 0:
        for each in range(len(agentsLs)):
            agentsLs[each].rl.save(directory, agentsName[each], i_episode)
            
    # 每隔几次输出一次信息
    if i_episode % print_log == 0 and i_episode != 0:
        # 输出回报
        print("Episode: {}, sum reward: {}".format(i_episode, np.sum(rewards)))

