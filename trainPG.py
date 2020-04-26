#-*- coding:utf-8 -*-

"""
训练神经网络
PG算法
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
    
    rewards0=[]
    log_probs0=[]
    entropies0=[]
    rewards1=[]
    log_probs1=[]
    entropies1=[]
    rewards2=[]
    log_probs2=[]
    entropies2=[]
    rewards3=[]
    log_probs3=[]
    entropies3=[]
    rewards4=[]
    log_probs4=[]
    entropies4=[]
    rewards5=[]
    log_probs5=[]
    entropies5=[]
    rewards6=[]
    log_probs6=[]
    entropies6=[]
    rewards7=[]
    log_probs7=[]
    entropies7=[]
    
    # 每次训练
    while True:
        password = input("按回车继续:")
        
        for each in env.envStates:
            print(each)
        
        env.count += 1
        # ===========Agent0操作===========
        init_flag = 0
        state = toInitialAgentState(env) # 环境state转换成agent的state
        if initialAgentChoose(agent0, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent0.taskNum):
                if state[eachTask] != 0:
                    if sum(state[agent0.taskNum+1:]) != agent0.machineNum:
                        
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent0.taskNum)
                        #print(s)
                        actionAll = [0]*agent0.machineNum
                        ls_episode[agent0.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent0.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        print("agent0")
                        print(s)
                        print(action)
                        print(reward)
                        entropies0.append(entropy)
                        log_probs0.append(log_prob)
                        rewards0.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
                            state[agent0.taskNum+action[0]-1] = 1
            states = env.initialStep(agent0, actionAll)
        else:
            action = [0]*agent0.machineNum
            states = env.initialStep(agent0, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        #password = input("按回车继续:")
        # ===========Agent1操作===========
        init_flag = 0
        state = toProcessAgentState(env, agent1) # 环境state转换成agent的state
        if processAgentChoose(agent1, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent1.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent1.lastMachineNum+1:]) != agent1.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent1.lastMachineNum)
                        
                        actionAll = [0]*agent1.machineNum
                        ls_episode[agent1.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent1.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies1.append(entropy)
                        log_probs1.append(log_prob)
                        rewards1.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent1, actionAll)
        else:
            action = [0]*agent1.machineNum
            states = env.processStep(agent1, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent2操作===========
        init_flag = 0
        state = toProcessAgentState(env, agent2) # 环境state转换成agent的state
        if processAgentChoose(agent2, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent2.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent2.lastMachineNum+1:]) != agent2.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent2.lastMachineNum)
                        
                        actionAll = [0]*agent2.machineNum
                        ls_episode[agent2.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent2.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies2.append(entropy)
                        log_probs2.append(log_prob)
                        rewards2.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent2, actionAll)
        else:
            action = [0]*agent2.machineNum
            states = env.processStep(agent2, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent3操作===========
        init_flag = 0
        state = toProcessAgentState(env, agent3) # 环境state转换成agent的state
        if processAgentChoose(agent3, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent3.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent3.lastMachineNum+1:]) != agent3.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent3.lastMachineNum)
                        
                        actionAll = [0]*agent3.machineNum
                        ls_episode[agent3.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent3.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies3.append(entropy)
                        log_probs3.append(log_prob)
                        rewards3.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent3, actionAll)
        else:
            action = [0]*agent3.machineNum
            states = env.processStep(agent3, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent4操作===========
        init_flag = 0
        state = toProcessAgentState(env, agent4) # 环境state转换成agent的state
        if processAgentChoose(agent4, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent4.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent4.lastMachineNum+1:]) != agent4.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent4.lastMachineNum)
                        
                        actionAll = [0]*agent4.machineNum
                        ls_episode[agent4.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent4.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies4.append(entropy)
                        log_probs4.append(log_prob)
                        rewards4.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent4, actionAll)
        else:
            action = [0]*agent4.machineNum
            states = env.processStep(agent4, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent5操作===========
        init_flag = 0
        state = toLastAgentState(env, agent5) # 环境state转换成agent的state
        if processAgentChoose(agent5, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent5.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent5.lastMachineNum+1:]) != agent5.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent5.lastMachineNum)
                        
                        actionAll = [0]*agent5.machineNum
                        ls_episode[agent5.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent5.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies5.append(entropy)
                        log_probs5.append(log_prob)
                        rewards5.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent5, actionAll)
        else:
            action = [0]*agent5.machineNum
            states = env.processStep(agent5, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent6操作===========
        init_flag = 0
        state = toLastAgentState(env, agent6) # 环境state转换成agent的state
        if processAgentChoose(agent6, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent6.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent6.lastMachineNum+1:]) != agent6.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent6.lastMachineNum)
                        
                        actionAll = [0]*agent6.machineNum
                        ls_episode[agent6.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent6.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies6.append(entropy)
                        log_probs6.append(log_prob)
                        rewards6.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent6, actionAll)
        else:
            action = [0]*agent6.machineNum
            states = env.processStep(agent6, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        # ===========Agent7操作===========
        init_flag = 0
        state = toLastAgentState(env, agent7) # 环境state转换成agent的state
        if processAgentChoose(agent7, state):
            # 满足下面条件agent便可以运行, 否则不可运行
            for eachTask in range(agent7.lastMachineNum):
                if state[eachTask] != 0:
                    if sum(state[agent7.lastMachineNum+1:]) != agent7.machineNum:
                        # 全局state转成局部state
                        s = allSToPartSInit(state, eachTask, agent7.lastMachineNum)
                        
                        actionAll = [0]*agent7.machineNum
                        ls_episode[agent7.processNum] += 1 # 记录迭代次数
                        
                        action, log_prob, entropy = agent7.rl.select_action(torch.Tensor([s])) # 选择动作
                        action = action.cpu()
                        reward, done = env.initReturn(s, action)
                        
                        entropies7.append(entropy)
                        log_probs7.append(log_prob)
                        rewards7.append(reward)
                        # 如果决策出错
                        if done:
                            init_flag = 1
                        if action[0] != 0:
                            actionAll[action[0]-1] = 1
            states = env.processStep(agent7, actionAll)
        else:
            action = [0]*agent7.machineNum
            states = env.processStep(agent7, action)
        env.envStates = states # 更新states
        if init_flag == 1:
            break
        
        
        # 调度系统正常完成
        if env.ifTaskFinish() == 1:
            #print("Decision succeed")
            break
    # ===========其它操作===========
    # update
    if len(rewards0) != 0:
        agent0.rl.update(rewards0, log_probs0, entropies0)
    if len(rewards1) != 0:
        agent1.rl.update(rewards1, log_probs1, entropies1)
    if len(rewards2) != 0:
        agent2.rl.update(rewards2, log_probs2, entropies2)
    if len(rewards3) != 0:
        agent3.rl.update(rewards3, log_probs3, entropies3)
    if len(rewards4) != 0:
        agent4.rl.update(rewards4, log_probs4, entropies4)
    if len(rewards5) != 0:
        agent5.rl.update(rewards5, log_probs5, entropies5)
    if len(rewards6) != 0:
        agent6.rl.update(rewards6, log_probs6, entropies6)
    if len(rewards7) != 0:
        agent7.rl.update(rewards7, log_probs7, entropies7)
            
    # save
    for each in range(len(agentsName)):
        if ls_episode[each] % log_interval == 0 and ls_episode[each] != 0:
            agentsLs[each].rl.save(directory, agentsName[each], ls_episode[each])
            
    # 每隔几次输出一次信息
    if i_episode % print_log == 0 and i_episode != 0:
        # 输出回报
        print("Episode: {}".format(i_episode))

