#-*- coding:utf-8 -*-

"""
test.py

使用随机算法决策, 运行调度系统, 显示ui, 测试系统可行性
"""

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
env.recordState() # 记录初始化
recordActions = [] # 记录各个时刻的actions

# 创建相关ui
app = QtWidgets.QApplication(sys.argv)
gui = MainUi()


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
    password = input("按回车继续:")
    # t时刻遍历所有agent一次
    env.count += 1
    tempActions = []
    
    # ===========InitialAgent操作===========
    state = toInitialAgentState(env) # 环境state转换成agent的state
    action = agent0.SelectActionRandom(state) # 选择动作
    # 环境反馈
    done = env.initialStep(agent0, action)
    reward = -env.count
    tempActions.append(action) # 记录InitialAgent操作
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
        done = env.processStep(eachAgent, action)
        reward = -env.count
        tempActions.append(action)
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
    done = env.finalStep(agent5, action, agent2, agent3, agent4)
    reward = -env.count
    tempActions.append(action)
    if done:
        reward = -1000
        print("Decision failure, task failure")
        break
        
    # 记录下每t时刻, 整个系统的的states和actions
    env.recordState()
    recordActions.append(tempActions)
    # recordActions存入txt文件
    # 待写
    
    gui.plotGantGraph(env.envStates, env.count) # 数据写入ui
    
    if env.ifTaskFinish() == 1:
        break

gui.show()
sys.exit(app.exec_())
