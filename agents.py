#-*- coding:utf-8 -*-

"""
agents.py

该程序实现了整个项目的环境
"""

# 进行决策的agent, 父类
class VanillaAgent:
    # 
    def __init__(self, processNum, machineNum):
        self.processNum = processNum
        self.machineNum = machineNum

    # 随机算法决策
    def SelectAction(self, state):
        pass


'''
最初处理原料的agent, 继承父类
state格式: 数组, 长度为task的种数, 元素的取值是剩下未完成的job数
action格式: 数组, 长度为machine数量, 元素取值范围是0-task的种数, 表示不选择动作或者选择task中的一个进行加工
'''
class InitialAgent(VanillaAgent):
    # 随机算法决策
    def SelectAction(self, state):
        pass
