#-*- coding:utf-8 -*-

"""
utils.py

工具类
"""

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
    