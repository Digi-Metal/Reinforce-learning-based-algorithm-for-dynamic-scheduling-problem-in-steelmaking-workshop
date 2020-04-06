#-*- coding:utf-8 -*-

"""
agents.py

该程序定义agent群
分两种agent: 加工原材料的agent和加工半成品的agent
"""

import random

# 进行决策的agent, 父类
class VanillaAgent:
    # 参数: 流程数, 设备数
    def __init__(self, processNum, machineNum):
        self.processNum = processNum
        self.machineNum = machineNum

    # 随机算法决策
    def SelectAction(self, state):
        pass


'''
最初处理原料的agent, 继承父类

state格式: list, 长度为task的种数(定值)+machine的数量(定值)
第一部分元素的取值是剩下未完成的job数(0-N)
第二部分取值是machine状态, 0是空闲, 1是非空闲/占用(工作中或工作结束但材料没运走或损坏)
例如(3,2,0,1)表示task1剩下3个job, task2剩下2个job, task3剩下0个job, machine1正在占用

action格式: list, 长度为machine数量(定值), 元素取值范围是0-task的种数, 表示不选择动作或者选择task中的一个进行加工, 0为不动作
例如(2,1,0)表示第一台设备运行一个task2的job,第二台设备运行一个task1的job,第三台设备不工作
'''
class InitialAgent(VanillaAgent):
    # 新增加一个Task的种类数
    def __init__(self, processNum, machineNum, taskNum):
        super().__init__(processNum, machineNum)
        self.taskNum = taskNum
    
    # 随机算法决策
    def SelectActionRandom(self, state):
        stateFront = state[: self.taskNum]
        action = []
        # 每个设备随机选择动作, 注意这里设备按编号顺序先后决策
        for each in range(self.machineNum):
            # 获得该设备的状态
            machineState = state[self.taskNum+each]
            # machine空闲且有可供选择的job时,有0.5概率动作,如果动作则挑一个不为0的task运行
            if machineState == 0 and sum(stateFront) != 0:
                # 动作
                if random.randint(0, 1) == 1:
                    # 挑一个不为0的task运行
                    noZeroList = [n for n in range(self.taskNum) if stateFront[n]>0 ]
                    tempIndex = random.choice(noZeroList)
                    action.append(tempIndex+1)
                    # 每台设备决策后都会state更新
                    stateFront[tempIndex] -= 1
                else:
                    action.append(0)
            else:
                action.append(0)
        return action


'''
中途处理原料的agent, 继承父类

state格式: list, 长度为上一个agent的machine数(定值)+本agent的machine数(定值)
第一部分元素取值: 上一个agent的machine的状态, 0是其他情况, taskNum是种类为taskNum的job运行完成
第二部分元素取值: 本agent的machine的状态, 0是空闲, 1是非空闲(工作中或工作结束但材料没运走或损坏)

action格式: list, 长度为machine数量(定值)
元素取值范围: 0+(lastAgent的Machine下标+1),
表示选择lastAgent的Machine的材料进行加工(要求材料在lastAgent上已经完工), 0表示不动作
'''
class ProcessAgent(VanillaAgent):
    # 新增加一个Task的种类数
    def __init__(self, processNum, machineNum, lastMachineNum):
        super().__init__(processNum, machineNum)
        self.lastMachineNum = lastMachineNum
    
    # 随机算法决策
    def SelectActionRandom(self, state):
        stateFront = state[: self.lastMachineNum]
        action = []
        for each in range(self.machineNum):
            # 设备不空闲或上一个流程没有job运行完的时候不动作
            if state[self.lastMachineNum+each] != 0 or sum(stateFront) == 0:
                action.append(0)
            else:
                # 设备空闲时有0.5概率动作, 从上一个流程里面选已经完成的job继续运行
                if random.randint(0, 1) == 1:
                    noZeroList = [n for n in range(self.lastMachineNum) if stateFront[n]>0 ]
                    tempIndex = random.choice(noZeroList)
                    action.append(tempIndex)
                    # 每台设备决策后都会state更新
                    stateFront[tempIndex] = 0
                else:
                    action.append(0)
        return action


# 测试程序
def main():
    agent0 = InitialAgent(0, 4, 3)
    agent1 = ProcessAgent(1, 6, 4)
    #state = [6,5,4,0,0,0,0]
    #action = agent0.SelectActionRandom(state)
    #print(action)
    state = [0,2,3,1, 0,0,0,0,0,0]
    action = agent1.SelectActionRandom(state)
    print(action)
    

if __name__ == '__main__':
    main()