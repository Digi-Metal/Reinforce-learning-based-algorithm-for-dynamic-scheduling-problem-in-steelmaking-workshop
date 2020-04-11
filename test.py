#-*- coding:utf-8 -*-

"""
test.py

使用随机算法决策, 运行调度系统, 显示ui, 测试系统可行性
"""

import copy
from ui import *
from utils import *
from environment import *

# 新建agent
agent0 = InitialAgent(0, 4, 3)
agent1 = ProcessAgent(1, 6, 4)
agent2 = ProcessAgent(2, 5, 6)
agent3 = ProcessAgent(3, 3, 5)
agent4 = ProcessAgent(4, 4, 3)
agent5 = FinalAgent(5, 4, 5, 3, 4)
processAgents = [agent1, agent2, agent3, agent4]

env = Env() # 新建环境
env.reset() # 环境重置
recordStates = [] # 记录各个时刻的states
recordStates.append(str(env.envStates))
recordActions = [] # 记录各个时刻的actions


'''
伪代码:
for t(count):
    for each_agent:
        (agent进行决策)
        selectAction
        return nextState, reward
        state = nextState
注意:
env的state和agent的state不一样, 使用前需要转换
'''
while True:
    #password = input("按回车继续:")
    # t时刻遍历所有agent一次
    env.count += 1
    tempActions = []
    
    # ===========InitialAgent操作===========
    state = toInitialAgentState(env) # 环境state转换成agent的state
    action = agent0.SelectActionRandom(state) # 选择动作
    # 环境反馈
    states, done = env.initialStep(agent0, action)
    reward = -env.count
    tempActions.append(action) # 记录InitialAgent操作
    env.envStates = states # 更新states
    # 如果系统出错
    if done:
        reward = -1000
        print("Decision failure, task failure")
        break
        
    # ===========processAgent依次操作===========
    flag = 0
    for eachAgent in processAgents:
        state = toProcessAgentState(env, eachAgent)
        action = eachAgent.SelectActionRandom(state)
        states, done = env.processStep(eachAgent, action)
        reward = -env.count
        tempActions.append(action)
        env.envStates = states
        if done:
            reward = -1000
            print("Decision failure, task failure")
            flag = 1
            break
    if flag == 1:
        break
    
    # ===========FinalAgent操作===========
    state = toFinalAgentState(env,agent2,agent3,agent4,agent5)
    action = agent5.SelectActionRandom(state)
    states, done = env.finalStep(agent5, action, agent2, agent3, agent4)
    reward = -env.count
    tempActions.append(action)
    env.envStates = states
    if done:
        reward = -1000
        print("Decision failure, task failure")
        break
        
    # =================显示=================
    print("===================")
    print("count:")
    print(env.count)
    print("------state------")
    for each in env.envStates:
        print(each)
    print("------action------")
    for each in tempActions:
        print(each)
    # =================显示=================
    
    # 记录下每t时刻, 整个系统的的states和actions
    recordStates.append(str(states))
    recordActions.append(str(tempActions))
    
    if env.ifTaskFinish() == 1:
        break

# 保存数据
writeData(recordStates, recordActions)

