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

伪代码:
for t(count):
    for each_agent:
        if agent要决策:
            agent进行决策
'''
class Env:
    # 定义一个调度系统, 以及5个task1, 6个task2, 4个task3
    def __init__(self):
        # 运行总时间
        self.count = 0
        self.schedulingSystem = SchedulingSystem()
        
    '''
    step功能包括:
    for each_agent:
            if agent要决策:
                agent进行决策
    '''
    def step(self):
        # 计数
        self.count += 1
        # 每个时间t内都对所有的agent进行遍历
        for each in len(self.schedulingSystem.processNum):
            pass
    
    # 
    def reset(self):
        pass