#-*- coding:utf-8 -*-

"""
训练神经网络
DDDPG算法
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
agent0 = InitialAgent(0, 4, 3, 0, 0.1, 500, device)
agent1 = ProcessAgent(1, 6, 4, 0, 0.1, 500, device)
agent2 = ProcessAgent(2, 5, 6, 0, 0.1, 500, device)
agent3 = ProcessAgent(3, 3, 5, 0, 0.1, 500, device)
agent4 = ProcessAgent(4, 4, 3, 0, 0.1, 500, device)
agent5 = LastAgent(5, 2, 4, 5, 0, 0.1, 500, device)
agent6 = LastAgent(5, 3, 4, 3, 0, 0.1, 500, device)
agent7 = LastAgent(5, 4, 4, 4, 0, 0.1, 500, device)

processAgents = [agent1, agent2, agent3, agent4]
lastAgents = [agent5, agent6, agent7]
agentsLs = [agent0, agent1, agent2, agent3, agent4, agent5, agent6, agent7]
agentsName = ['agent0', 'agent1', 'agent2', 'agent3', 'agent4', 'agent5', 'agent6', 'agent7']
ls_episode = [0, 0, 0, 0, 0, 0, 0, 0]


# 参数
num_episodes = 10000     # 训练多少次
retrain = True        # 是否重头训练
weight_num = 900        # 载入权重的代数,用于中途继续训练
log_interval = 100       # 每隔log_interval保存一次参数
print_log = 1       # 每走print_log次输出一次

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
        env.count += 1
        '''
        print('-------count-------')
        print(env.count)
        print('-------envStates-------')
        for each in env.envStates:
            print(each)
        '''
        # ===========InitialAgent操作===========
        init_flag = 0
        state = toInitialAgentState(env) # 环境state转换成agent的state
        # InitialAgent是否要操作
        if initialAgentChoose(agent0, state):
            '''
            password = input("按回车继续:")
            print('agent num')
            print(agent0.processNum)
            print('envStates: ')
            for each in env.envStates:
                print(each)
            '''
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent0.taskNum):
                if state[eachTask] != 0:
                    if sum(state[agent0.taskNum+1:]) != agent0.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent0.taskNum)
                        actionAll = [0]*agent0.machineNum
                        ls_episode[agent0.processNum] += 1 # 记录迭代次数
                        action = agent0.rl.select_action(s) # 选择动作
                        action = agent0.rl.add_action_noise(action) # add noise to action
                        reward, done = env.initReturn(s, action)
                        '''
                        password = input("按回车继续:")
                        print('state: ')
                        print(s)
                        print('action: ')
                        print(action)
                        print("reward: ")
                        print(reward)
                        print("done: ")
                        print(done)
                        '''
                        rewards.append(reward) # 记录各步骤reward
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
                            state[agent0.taskNum+action[0]-1] = 1
                        next_s = allSToPartSInit(state, eachTask, agent0.taskNum)
                        # 数据添加入replay_buffer
                        agent0.rl.replay_buffer.push((s, next_s, action[0], reward, np.float(done)))
            states = env.initialStep(agent0, actionAll)
            env.envStates = states
            '''
            print('envStates: ')
            for each in env.envStates:
                print(each)
            '''
        else:
            action = [0]*agent0.machineNum
            states, reward, done = env.initialStep(agent0, action)
            env.envStates = states # 更新states
            
        if init_flag == 1:
            break
        # ===========processAgent依次操作===========
        flag = 0
        for eachAgent in processAgents:
            process_flag = 0
            state = toProcessAgentState(env, eachAgent)
            
            # processAgent是否要操作
            if processAgentChoose(eachAgent, state):
                '''
                password = input("按回车继续:")
                print('agent num')
                print(eachAgent.processNum)
                print('state')
                print(state)
                print('envStates: ')
                for each in env.envStates:
                    print(each)
                '''
                # 满足下面条件agent便可以运行, 否则不可运行
                for eachTask in range(eachAgent.lastMachineNum):
                    if state[eachTask] != 0:
                        if sum(state[eachAgent.lastMachineNum+1:]) != eachAgent.machineNum:
                            # 全局state转成局部state
                            s = allSToPartSInit(state, eachTask, eachAgent.lastMachineNum)
                            actionAll = [0]*eachAgent.machineNum
                            ls_episode[eachAgent.processNum] += 1 # 记录迭代次数
                            action = eachAgent.rl.select_action(s) # 选择动作
                            action = eachAgent.rl.add_action_noise(action) # add noise to action
                            reward, done = env.initReturn(s, action)
                            '''
                            print('state: ')
                            print(s)
                            print('action: ')
                            print(action)
                            print("reward: ")
                            print(reward)
                            print("done: ")
                            print(done)
                            '''
                            rewards.append(reward) # 记录各步骤reward
                            # 如果决策出错
                            if done:
                                init_flag = 1
                            if action[0] != 0:
                                actionAll[action[0]-1] = 1
                                state[eachAgent.lastMachineNum+action[0]-1] = 1
                            next_s = allSToPartSInit(state, eachTask, eachAgent.lastMachineNum)
                            # 数据添加入replay_buffer
                            eachAgent.rl.replay_buffer.push((s, next_s, action[0], reward, np.float(done)))
                states = env.processStep(eachAgent, actionAll)
                env.envStates = states
                '''
                print('envStates: ')
                for each in env.envStates:
                    print(each)
                '''
            else:
                action = [0]*eachAgent.machineNum
                states = env.processStep(eachAgent, action)
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
            
            # processAgent是否要操作
            if processAgentChoose(eachAgent, state):
                '''
                password = input("按回车继续:")
                print('agent num')
                print(eachAgent.processNum)
                print('state: ')
                print(state)
                print('envStates: ')
                for each in env.envStates:
                    print(each)
                '''
                # 满足下面条件agent便可以运行, 否则不可运行
                for eachTask in range(eachAgent.lastMachineNum):
                    if state[eachTask] != 0:
                        if sum(state[eachAgent.lastMachineNum+1:]) != eachAgent.machineNum:
                            # 全局state转成局部state
                            s = allSToPartSInit(state, eachTask, eachAgent.lastMachineNum)
                            actionAll = [0]*eachAgent.machineNum
                            ls_episode[eachAgent.processNum] += 1 # 记录迭代次数
                            action = eachAgent.rl.select_action(s) # 选择动作
                            action = eachAgent.rl.add_action_noise(action) # add noise to action
                            reward, done = env.initReturn(s, action)
                            '''
                            print('state: ')
                            print(s)
                            print('action: ')
                            print(action)
                            print("reward: ")
                            print(reward)
                            print("done: ")
                            print(done)
                            '''
                            rewards.append(reward) # 记录各步骤reward
                            # 如果决策出错
                            if done:
                                init_flag = 1
                            if action[0] != 0:
                                actionAll[action[0]-1] = 1
                                state[eachAgent.lastMachineNum+action[0]-1] = 1
                            next_s = allSToPartSInit(state, eachTask, eachAgent.lastMachineNum)
                            # 数据添加入replay_buffer
                            eachAgent.rl.replay_buffer.push((s, next_s, action[0], reward, np.float(done)))
                states = env.processStep(eachAgent, actionAll)
                env.envStates = states
                '''
                print('envStates: ')
                for each in env.envStates:
                    print(each)
                '''
            else:
                action = [0]*eachAgent.machineNum
                states, reward, done = env.lastStep(eachAgent, action)
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
    for each in range(len(agentsName)):
        if ls_episode[each] % log_interval == 0 and ls_episode[each] != 0:
            agentsLs[each].rl.save(directory, agentsName[each], ls_episode[each])
            
    # 每隔几次输出一次信息
    if i_episode % print_log == 0 and i_episode != 0:
        # 输出回报
        print("Episode: {}, sum reward: {}".format(i_episode, np.sum(rewards)))

