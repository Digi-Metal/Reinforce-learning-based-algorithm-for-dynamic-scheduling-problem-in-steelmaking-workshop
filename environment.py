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
        # 已完成的任务
        self.finishTask = [0,0,0]
        
        # 记录实时states和累计states
        self.envStates = []
        
        # 定义task
        self.taskType = 3
        self.task1 = Task()
        self.task2 = TaskTwo()
        self.task3 = TaskThree()
    
    # 辅助程序
    def runTime(self, taskType, m, n):
        if taskType == 1:
            return self.task1.dealTime(self.task1.dealArray, m, n)
        elif taskType == 2:
            return self.task2.dealTime(self.task2.dealArray, m, n)
        elif taskType == 3:
            return self.task3.dealTime(self.task3.dealArray, m, n)
    
    # 辅助程序
    def transTime(self, processNum, m, n):
        if processNum == 1:
            return self.schedulingSystem.transpotTime(self.schedulingSystem.process0.transpotArray, m, n)
        elif processNum == 2:
            return self.schedulingSystem.transpotTime(self.schedulingSystem.process1.transpotArray, m, n)
        elif processNum == 3:
            return self.schedulingSystem.transpotTime(self.schedulingSystem.process2.transpotArray, m, n)
        elif processNum == 4:
            return self.schedulingSystem.transpotTime(self.schedulingSystem.process3.transpotArray, m, n)
    
    # 辅助程序
    def transCrossTime(self, taskType, m, n):
        if taskType == 1:
            return self.task1.dealTime(self.task1.transport2To5, m, n)
        elif taskType == 2:
            return self.task2.dealTime(self.task2.transport3To5, m, n)
        elif taskType == 3:
            return self.schedulingSystem.transpotTime(self.schedulingSystem.process4.transpotArray, m, n)
    
    
    '''
    定义initialStep的States规则:
    原料列表: 值表示还剩下多少任务没有开工
    各agent列表分以下情况:
    -1: 损坏/维护, 格式: [-1]
    0: 空闲, 格式: [0]
    1: 工作, 格式:[1, task, 结束倒计时, 1(延时)/0(正常)/-1(提早)]
        eg: [1, 2, 5, 0] 表示: 当前machine运行task2, 5t后工作结束, 目前一切正常
    3: 占用, 格式: [3]
    没有运输环节
    '''
    # 输入action, 更改envStates, done表示系统是否出错
    def initialStep(self, agent, action):
        done = 0
        envStates = self.envStates
        # 原料的state与本agent的state变化
        material = envStates[0]
        state = envStates[agent.processNum+1]
        
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
                    temp = self.runTime(action[each],agent.processNum,each)
                    state[each] = [1, action[each], temp, 0]
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
                        temp = state[each][1]
                        state[each] = [3, temp]
        
        envStates[0] = material
        envStates[agent.processNum+1] = state
        
        return envStates, done
        
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
        envStates = self.envStates
        # 上一个agent的state与本agent的state变化
        lastState = envStates[agent.processNum]
        state = envStates[agent.processNum+1]
        
        # 对每一个设备分析情况
        for each in range(agent.machineNum):
            # 设备为损坏或维护时
            if state[each][0] == -1:
                # 损坏或维护不能添加任务
                if action[each] != 0:
                    done = 1
                    break
            # lastMachine=3且设备为空闲时可以添加任务, lastMachine由占用状态变运输状态
            elif state[each][0] == 0:
                if action[each] != 0:
                    if lastState[action[each]-1][0] == 3:
                        # agent3不能选task1
                        if agent.processNum == 3 and lastState[action[each]-1][-1] == 1:
                            done = 1
                            break
                        # agent4不能选task1和task2, 只能选task3
                        if agent.processNum == 4 and lastState[action[each]-1][-1] != 3:
                            done = 1
                            break
                        temp = self.transTime(agent.processNum,action[each]-1,each)
                        state[each] = [2, lastState[action[each]-1][-1], action[each]-1, each, temp]
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
                    # 运输到目的地转为工作状态
                    if state[each][-1] == 0:
                        temp = self.runTime(state[each][1],agent.processNum,each)
                        state[each] = [1, state[each][1], temp, 0]
        
        envStates[agent.processNum] = lastState
        envStates[agent.processNum+1] = state
        
        return envStates, done
        
    '''
    定义finalStep的States规则:
    和processStep原则一样, 多了一个完成任务的记录
    '''
    def finalStep(self, agent, action, agent2, agent3, agent4):
        done = 0
        envStates = self.envStates
        agent2State = envStates[agent.processNum-2]
        agent3State = envStates[agent.processNum-1]
        agent4State = envStates[agent.processNum]
        state = envStates[agent.processNum+1]
        
        # 对每一个设备分析情况
        for each in range(agent.machineNum):
            # 设备为损坏或维护时
            if state[each][0] == -1:
                # 损坏或维护不能添加任务
                if action[each] != 0:
                    done = 1
                    break
            # 设备为空闲时可以添加任务
            elif state[each][0] == 0:
                if action[each] != 0:
                    # 对action进行解码, 区分action获取哪个agent的job
                    tempActAg3 = action[each]-agent2.machineNum
                    tempActAg4 = action[each]-agent2.machineNum-agent3.machineNum
                    # agent2部分
                    if action[each] < (agent2.machineNum+1):
                        if agent2State[action[each]-1][0] == 3:
                            temp = self.transCrossTime(agent2State[action[each]-1][-1],action[each]-1,each)
                            state[each] = [2, agent2State[action[each]-1][-1], action[each]-1, each, temp]
                            agent2State[action[each]-1] = [0]
                        else:
                            done = 1
                            break
                    # agent3部分
                    elif action[each] < (agent2.machineNum+agent3.machineNum+1):
                        if agent3State[tempActAg3-1][0] == 3:
                            temp = self.transCrossTime(agent3State[tempActAg3-1][-1],tempActAg3-1,each)
                            state[each] = [2, agent3State[tempActAg3-1][-1], tempActAg3-1, each, temp]
                            agent3State[tempActAg3-1] = [0]
                        else:
                            done = 1
                            break
                    # agent4部分
                    else:
                        if agent4State[tempActAg4-1][0] == 3:
                            temp = self.transCrossTime(agent4State[tempActAg4-1][-1],tempActAg4-1,each)
                            state[each] = [2, agent4State[tempActAg4-1][-1], tempActAg4-1, each, temp]
                            agent4State[tempActAg4-1] = [0]
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
                    # 工作完成时变成空闲
                    if state[each][2] == 0:
                        self.finishTask[state[each][1]-1] += 1
                        state[each] = [0]
            # 设备为运输时不能选动作
            elif state[each][0] == 2:
                if action[each] != 0:
                    done = 1
                    break
                # 运输时间减1
                else:
                    state[each][-1] -= 1
                    # 运输到目的地转为工作状态
                    if state[each][-1] == 0:
                        temp = self.runTime(state[each][1],agent.processNum,each)
                        state[each] = [1, state[each][1], temp, 0]
        
        envStates[agent.processNum-2] = agent2State
        envStates[agent.processNum-1] = agent3State
        envStates[agent.processNum] = agent4State
        envStates[agent.processNum+1] = state
        
        return envStates, done
        
    # 重置时间与状态
    def reset(self):
        self.count = 0
        self.finishTask = [0,0,0]
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
            if each != 0:
                return 0
        # 过程全为0或者-1
        for eachLine in process:
            for each in eachLine:
                if each[0] != 0 and each[0] != -1:
                    return 0
        print("调度结束")
        return 1
        
