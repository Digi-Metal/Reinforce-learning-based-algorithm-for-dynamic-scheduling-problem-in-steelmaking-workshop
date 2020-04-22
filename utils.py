#-*- coding:utf-8 -*-

"""
utils.py

工具类
"""

import os
import time

# 环境的state转换成initial agent的state
def toInitialAgentState(env):
    state = []
    for each in env.envStates[0]:
        state.append(each)
    for each in env.envStates[1]:
        if each[0] == 0:
            state.append(0)
        else:
            state.append(1)
    return state

# 环境的state转换成process agent的state
def toProcessAgentState(env, agent):
    state = []
    # last agent
    for each in env.envStates[agent.processNum]:
        if each[0] == 3:
            state.append(each[-1])
        else:
            state.append(0)
    # this agent
    for each in env.envStates[agent.processNum+1]:
        if each[0] == 0:
            state.append(0)
        else:
            state.append(1)
    return state
    
# 环境的state转换成final agent的state
def toFinalAgentState(env,agent2,agent3,agent4,agent5):
    state = []
    for each in env.envStates[agent2.processNum+1]:
        if each[0] == 3:
            state.append(each[-1])
        else:
            state.append(0)
    for each in env.envStates[agent3.processNum+1]:
        if each[0] == 3:
            state.append(each[-1])
        else:
            state.append(0)
    for each in env.envStates[agent4.processNum+1]:
        if each[0] == 3:
            state.append(each[-1])
        else:
            state.append(0)
    # this agent
    for each in env.envStates[agent5.processNum+1]:
        if each[0] == 0:
            state.append(0)
        else:
            state.append(1)
    return state

# 环境的state转换成last agent的state
def toLastAgentState(env, agent):
    state = []
    # last agent
    for each in env.envStates[agent.lastProcessNum+1]:
        if each[0] == 3 and each[-1] == (agent.lastProcessNum-1):
            state.append(each[-1])
        else:
            state.append(0)
    # this agent
    for each in env.envStates[agent.processNum+1]:
        if each[0] == 0:
            state.append(0)
        else:
            state.append(1)
    return state

'''
recordState和recordActions存入txt文件
文件名: 用当前时间来命名
内有两个txt文件, 分别储存state和action数据
state是从t=0开始的
action从t=0至t=1之间决策,所以数量比state少1
'''
def writeData(recordStates, recordActions):
    now = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime(time.time()))
    filename = "record/record_" + now + "/"
    if not os.path.exists(filename):
        # 目录不存在, 进行创建操作
        os.makedirs(filename)
    with open(filename + "/state_record.txt", 'w') as f:
        for eachTimeState in recordStates:
            f.write(eachTimeState)
            f.write("\n")
    with open(filename + "action_record.txt", 'w') as f:
        for eachAction in recordActions:
            f.write(eachAction)
            f.write("\n")

# initialAgent是否需要进行动作
def initialAgentChoose(agent, state):
    stateFront = state[: agent.taskNum]
    machineState = state[agent.taskNum :]
    if sum(stateFront) == 0:
        return 0
    elif sum(machineState) == agent.machineNum:
        return 0
    else:
        return 1

# processAgent是否需要进行动作
def processAgentChoose(agent, state):
    stateFront = state[: agent.lastMachineNum]
    machineState = state[agent.lastMachineNum :]
    if sum(stateFront) == 0:
        return 0
    elif sum(machineState) == agent.machineNum:
        return 0
    else:
        return 1
