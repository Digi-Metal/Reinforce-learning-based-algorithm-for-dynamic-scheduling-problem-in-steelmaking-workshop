#-*- coding:utf-8 -*-

"""
environment.py

该程序实现了整个项目的环境
"""

from background import *
from agents import *

'''
整个运行环境, 原理:
时间不断增加, 时间不是现实时间, 而是count表示的计数
每一个时间, 对每一个agent进行遍历
每一个agent决策此时此刻是否要进行动作, 如何进行动作
一个agent决策后state变化后才轮到下一个agent进行决策
'''
class Env:
    # 定义一个调度系统, 以及5个task1, 6个task2, 4个task3
    def __init__(self):
        self.schedulingSystem = SchedulingSystem()
        
        # 运行总时间
        self.count = 0
        
        # 记录实时states和累计states
        self.envStates = []
        self.recordStates = []
        
        # 定义task
        self.taskType = 3
        self.task1 = Task()
        self.task2 = TaskTwo()
        self.task3 = TaskThree()
    
    # 辅助程序
    def runTime(self, taskType, m, n):
        if taskType == 1:
            return self.task1.dealTime(task1.dealArray, m, n)
        elif taskType == 2:
            return self.task2.dealTime(task2.dealArray, m, n)
        elif taskType == 3:
            return self.task3.dealTime(task3.dealArray, m, n)
    
    # 记录当前的states
    def recordStates(self):
        self.recordStates.append(self.envStates)
        
    '''
    定义initialStep的States规则:
    原料列表: 值表示还剩下多少任务没有开工
    各agent列表分以下情况:
    -1: 损坏/维护, 格式: [-1]
    0: 空闲, 格式: [0]
    1: 工作, 格式:[1, task, 结束倒计时, 1(延时)/0(正常)/-1(提早)]
        eg: [1, 2, 5, 0] 表示: 当前machine运行task2, 5t后工作结束, 目前一切正常
    3: 占用, 格式: [3]
    '''
    # 输入action, 更改envStates, done表示系统是否出错
    def initialStep(self, agent, action):
        done = 0
        # 原料的state与本agent的state变化
        material = self.envStates[0]
        state = self.envStates[agent.processNum+1]
        
        # 对每一个设备分析情况
        for each in range(agent.machineNum):
            # 设备为损坏或维护时
            if state[each][0] == -1:
                # 损坏或维护不能添加任务
                if action[each] != 0:
                    done = 1
                    break
            # 设备为空闲时
            elif state[each][0] == 0:
                # 空闲时可以添加任务
                if action[each] != 0:
                    state[each] = [1, action[each], runTime(action[each],agent.processNum,each), 0]
                    material[action[each]-1] -= 1
            # 设备为工作时
            elif state[each][0] == 1:
                # 工作时不能添加任务
                if action[each] != 0:
                        done = 1
                        break
                else:
                    # 已有工作减1单位剩余时间
                    state[each][2] -= 1
                    # 工作完成时变成占用
                    if state[each][2] == 0:
                        state[each] = [3]
        
        self.envStates[0] = material
        self.envStates[agent.processNum+1] = state
        
        return done
        
    '''
    定义processStep的States规则:
    原料列表: 值表示还剩下多少任务没有开工
    各agent列表分以下情况:
    -1: 损坏/维护, 格式: [-1]
    0: 空闲, 格式: [0]
    1: 工作, 格式:[1, task, 结束倒计时, 1(延时)/0(正常)/-1(提早)]
        eg: [1, 2, 5, 0] 表示: 当前machine运行task2, 5t后工作结束, 目前一切正常
    2: 运输, 格式:[2, task, lastMachine, nextMachine, 结束倒计时]
        eg: [2, 2, 3, 4, 1] 表示: 正在将task2从machine4运往下个agent的machine5, 1t后到达
    3: 占用, 格式: [3, task]
    '''
    # 输入action, 更改envStates, done表示系统是否出错
    def processStep(self, agent, action):
        done = 0
        # 上一个agent的state与本agent的state变化
        lastState = self.envStates[agent.processNum]
        state = self.envStates[agent.processNum+1]
        
        # 对每一个设备分析情况
        for each in range(agent.machineNum):
            # 设备为损坏或维护时
            if state[each][0] == -1:
                # 损坏或维护不能添加任务
                if action[each] != 0:
                    done = 1
                    break
            # 设备为空闲时可以添加任务, lastMachine由占用状态变运输状态
            elif state[each][0] == 0:
                # 只有lastMachine=3且设备为空闲时才可以被选择
                if action[each] != 0 and lastState[action[each]-1][0] == [3]:
                    state[each] = [2, action[each], 3, 4, 1]]
                    lastState[action[each]-1] = [0]
                else:
                    done = 1
                    break
            # 设备为工作时
            elif state[each][0] == 1:
                # 工作时不能添加任务
                if action[each] != 0:
                        done = 1
                        break
                else:
                    # 已有工作减1单位剩余时间
                    state[each][2] -= 1
                    # 工作完成时变成占用
                    if state[each][2] == 0:
                        temp = state[each][1]
                        state[each] = [3, temp]
            # 设备为运输时不能选动作
            elif state[each][0] == 2:
                if action[each] != 0:
                    done = 1
                    break
                # 运输时间减1
                else:
                    state[each][-1] -= 1
        
        self.envStates[agent.processNum] = lastState
        self.envStates[agent.processNum+1] = state
        
        return done
        
    # 重置时间与状态
    def reset(self):
        self.count = 0
        self.envStates = [[5,6,4],
                          [[0],[0],[0],[0]],
                          [[0],[0],[0],[0],[0],[0]],
                          [[0],[0],[0],[0],[0]],
                          [[0],[0],[0]],
                          [[0],[0],[0],[0]],
                          [[0],[0],[0],[0]]]
    
    # 检查整个系统是否结束
    def ifTaskFinish(self):
        material = self.envStates[0]
        process = self.envStates[1:]
        # 原料不为0一定不完成
        for each in material:
            if each != 0
                return 0
        # 过程全为0或者-1
        for eachLine in process:
            for each in eachLine:
                if each[0] != 0 and each[0] != -1
                    return 0
        return 1
        
