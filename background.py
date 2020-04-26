#-*- coding:utf-8 -*-

"""
background.py

该程序定义了调度系统的各种信息, 包括 结构, 功能, 流程数量, 工艺种类等信息
包括: 6个流程组成的工艺系统, 三种任务

注意: 这里面所有的编号都是从0开始的
"""

import numpy as np

# 一个工业流程
class TechnologicalProcess:
    def __init__(self, machine):
        # 一个流程拥有的设备数
        self.machine = machine


# 整个调度系统
class SchedulingSystem:
    # 创建六个流程组成的调度系统
    def __init__(self):
        self.processNum = 6
        self.process0 = TechnologicalProcess(4)
        self.process1 = TechnologicalProcess(6)
        self.process2 = TechnologicalProcess(5)
        self.process3 = TechnologicalProcess(3)
        self.process4 = TechnologicalProcess(4)
        self.process5 = TechnologicalProcess(4)
        
        '''
        该流程的设备的材料 运输到 下一个流程的设备 的运输时间
        注意: 这个运输时间与材料无关, 无论是什么材料, 都是同样的运输时间
        
        数组形式, 行数为本流程设备数, 列数为下一个流程的设备数
        假设本流程machine=4, 下一个流程machine=3, 数组为4*3形式,
        array[02]表示本流程第0个machine的材料运输到下一个流程的第2个machine所需要的时间
        '''
        self.process0.transpotArray = np.array([[3, 7, 7, 8, 5, 5],
                                                [3, 9, 3, 4, 3, 3],
                                                [9, 3, 3, 4, 8, 4],
                                                [7, 7, 2, 9, 5, 2]])
        self.process1.transpotArray = np.array([[5, 4, 6, 6, 6],
                                                [9, 8, 9, 3, 6],
                                                [2, 2, 8, 7, 8],
                                                [8, 7, 5, 8, 9],
                                                [7, 4, 5, 2, 3],
                                                [9, 2, 3, 9, 2]])
        self.process2.transpotArray = np.array([[9, 5, 4],
                                                [4, 6, 8],
                                                [9, 6, 5],
                                                [2, 5, 5],
                                                [8, 4, 6]])
        self.process3.transpotArray = np.array([[3, 9, 6, 5],
                                                [6, 4, 3, 3],
                                                [8, 7, 8, 4]])
        self.process4.transpotArray = np.array([[6, 2, 4, 2],
                                                [8, 8, 6, 2],
                                                [3, 2, 9, 3],
                                                [5, 4, 6, 3]])

    # 材料从当前流程的设备m运输到下一个流程的设备n所需的时间
    def transpotTime(self, array, m, n):
        return array[m][n]


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
        0表示不在上面运行
        '''
        self.dealArray = np.array([[19, 15, 10, 15],
                                   [11, 16, 17, 19, 19, 13],
                                   [15, 11, 13, 16, 14],
                                   [0 , 0 , 0 ],
                                   [0 , 0 , 0 , 0 ],
                                   [15, 19, 10, 15]])
        
        '''
        工序3运输到工序6的时间, 结构和transpotArray一样
        '''
        self.transport2To5 = np.array([[12, 23, 24, 14],
                                       [24, 28, 13, 27],
                                       [19, 10, 11, 15],
                                       [16, 27, 17, 29],
                                       [11, 29, 21, 11]])
        
    # 返回该任务的材料在工序m的第n台设备运行所需要的时间
    def dealTime(self, array, m, n):
        return array[m][n]


# 继承父类Task, 其它一样，需要完成的任务, 任务二
class TaskTwo(Task):
    def __init__(self):
        self.process = '111101'
        self.dealArray = np.array([[16, 19, 10, 13],
                                   [10, 17, 19, 15, 12, 12],
                                   [14, 19, 14, 15, 19],
                                   [10, 18, 15],
                                   [0 , 0 , 0 , 0 ],
                                   [19, 12, 15, 10]])
        self.transport3To5 = np.array([[12,  6, 15,  8],
                                       [ 8, 11, 18, 11],
                                       [ 9,  7, 17, 16]])


# 继承父类Task, 其它一样，需要完成的任务, 任务三
class TaskThree(Task):
    def __init__(self):
        self.process = '111111'
        self.dealArray = np.array([[17, 10, 11, 15],
                                   [10, 19, 15, 15, 14, 11],
                                   [12, 18, 15, 12, 14],
                                   [15, 10, 16],
                                   [19, 15, 17, 18],
                                   [14, 17, 19, 12]])

