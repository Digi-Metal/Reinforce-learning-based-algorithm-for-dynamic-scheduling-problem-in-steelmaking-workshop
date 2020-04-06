#-*- coding:utf-8 -*-

"""
test.py

运行调度系统, 显示ui
"""

from environment import *
from utils import *

# 新建agent
agent0 = InitialAgent(0, 4, 3)
agent1 = ProcessAgent(1, 6, 4)
agent2 = ProcessAgent(2, 5, 6)
agent3 = ProcessAgent(3, 3, 5)
agent4 = ProcessAgent(4, 4, 3)
agent5 = ProcessAgent(5, 4, 4)
processAgents = [agent1, agent2, agent3, agent4, agent5]

# 新建环境
env = Env()
# 环境重置
env.reset()
# 记录初始化
env.recordStates()
# 记录各个时刻的actions
recordActions = []

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
    # t时刻遍历所有agent一次
    env.count += 1
    tempActions = []
    
    # 环境的state转换成agent的state
    state = toInitialAgentState(env)
    
    # InitialAgent操作
    action = agent0.SelectActionRandom(state)
    done = env.initialStep(agent, action)
    reward = -env.count
    # 记录InitialAgent操作
    tempActions.append(action)
    # 如果系统出错
    if done:
        reward = -1000
        print("Decision failure, task failure")
        break
        
    # processAgent依次操作
    for eachAgent in processAgents:
        # 环境的state转换成agent的state
        state = toProcessAgentState(env, eachAgent)
        
        action = eachAgent.SelectActionRandom(state)
        done = env.processStep(action)
        reward = -env.count
        # 记录processAgent操作
        tempActions.append(action)
        # 如果系统出错
        if done:
            reward = -1000
            print("Decision failure, task failure")
            break
            
    # 记录下每t时刻, 整个系统的的states和actions
    env.recordStates()
    recordActions.append(tempActions)
    # actions存入txt文件
    # 待写
    
    if env.ifTaskFinish() = 1:
        break
    