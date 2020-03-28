#-*- coding:utf-8 -*-

"""
background.py

该程序定义了调度系统的各种信息, 包括 结构, 功能, 流程数量, 工艺种类等信息
包括: 6个流程组成的工艺系统, 三种任务

注意: 这里面所有的编号都是从0开始的
"""

import numpy as np

# 一个工业流程 technological process
class TechnologicalProcess:
    def __init__(self, machine):
        # 一个流程拥有的设备数
        self.machine = machine
    
    # 材料从当前流程的设备m运输到下一个流程的设备n所需的时间
    def transpotTime(self, array, m, n):
        return array[m, n]


# 整个调度系统
class SchedulingSystem:
    # 创建六个流程组成的调度系统
    def __init__(self):
        self.processNum = 6
        process0 = TechnologicalProcess(4)
        process1 = TechnologicalProcess(6)
        process2 = TechnologicalProcess(5)
        process3 = TechnologicalProcess(3)
        process4 = TechnologicalProcess(4)
        process5 = TechnologicalProcess(4)
        
        '''
        该流程的设备的材料 运输到 下一个流程的设备 的运输时间
        注意: 这个运输时间与材料无关, 无论是什么材料, 都是同样的运输时间
        
        数组形式, 行数为本流程设备数, 列数为下一个流程的设备数
        假设本流程machine=4, 下一个流程machine=3, 数组为4*3形式,
        array[02]表示本流程第0个machine的材料运输到下一个流程的第2个machine所需要的时间
        '''
        process0.transpotArray = np.array([[46, 51, 14, 21, 79, 32],
                                           [63, 16, 36, 42, 60, 31],
                                           [59, 19, 55, 16, 27, 44],
                                           [23, 76, 73, 42, 51, 47]])
        process1.transpotArray = np.array([[62, 64, 74, 51, 17],
                                           [45, 80, 44, 25, 71],
                                           [64, 32, 50, 70, 54],
                                           [44, 44, 35, 49, 22],
                                           [57, 45, 62, 53, 35],
                                           [48, 28, 47, 73, 29]])
        process2.transpotArray = np.array([[24, 65, 20],
                                           [22, 61, 28],
                                           [54, 37, 60],
                                           [15, 30, 50],
                                           [45, 13, 48]])
        process3.transpotArray = np.array([[64, 27, 79, 12],
                                           [59, 12, 57, 10],
                                           [22, 32, 30, 58]])
        process4.transpotArray = np.array([[41, 13, 59, 25],
                                           [33, 20, 51, 78],
                                           [73, 39, 70, 51],
                                           [53, 52, 45, 59]])


'''
新建三个任务类型
'''
# 需要完成的任务, 任务一
class Task:
    def __init__(self):
        '''
        process由六个bool类型组成, 因为是6道工序所以是6个bool值, 工序数与bool数量一致
        111001表示要经过第1,2,3,6一共四道工序, 0表示该不需要经过该工序, 1表示需要经过该工序
        '''
        self.process = '111001'
        '''
        该任务的材料在设备上运行所需要的时间, 数组形式, 行为任务需要的工序数, 列为该工序的机器数
        假设需要4道工序, 每道工序的设备数分别为4654, 则有以下形式,
        array[02]表示材料在第1道工序的第3台设备上运行所需要的时间
        '''
        self.dealArray = np.array([[91, 43, 28, 45],
                                   [34, 75, 65, 97, 94, 50],
                                   [87, 61, 42, 76, 53],
                                   [76, 90, 49, 76]])
    
    # 返回该任务的材料在工序m的第n台设备运行所需要的时间
    def dealTime(self, array, m, n):
        return array[m, n]


# 继承父类Task, 其它一样，需要完成的任务, 任务二
class TaskTwo(Task):
    def __init__(self):
        self.process = '111101'
        self.dealArray = np.array([[51, 37, 50, 34],
                                   [64, 63, 31, 37, 65, 50],
                                   [65, 69, 46, 50, 60],
                                   [37, 57, 56],
                                   [51, 45, 48, 41]])
    
    def dealTime(self, array, m, n):
        return array[m, n]


# 继承父类Task, 其它一样，需要完成的任务, 任务三
class TaskThree(Task):
    def __init__(self):
        self.process = '111111'
        self.dealArray = np.array([[108, 86, 111, 76],
                                   [92, 117, 92, 118, 54, 58],
                                   [66, 114, 62, 57, 117],
                                   [62, 79, 71],
                                   [108, 101, 87, 114],
                                   [74, 53, 84, 80]])
    
    def dealTime(self, array, m, n):
        return array[m, n]


