#-*- coding:utf-8 -*-

"""
定义调度系统的程序, 调度系统的信息, 结构, 功能都在该程序里面被定义
该程序定义了一个6个流程组成的工艺系统

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

# 需要完成的任务
class 

# 整个调度系统
class Env:
    def __init__(self):
        # 创建六个流程组成的调度系统
        process0 = TechnologicalProcess(4)
        process1 = TechnologicalProcess(3)
        process2 = TechnologicalProcess(5)
        process3 = TechnologicalProcess(6)
        process4 = TechnologicalProcess(4)
        process5 = TechnologicalProcess(4)
        
        '''
        该流程的设备的材料 运输到 下一个流程的设备 的运输时间
        注意: 这个运输时间与材料无关, 无论是什么材料, 都是同样的运输时间
        
        数组形式, 行数为本流程设备数, 列数为下一个流程的设备数
        假设本流程machine=4, 下一个流程machine=3, 数组为4*3形式,
        array[02]表示本流程第0个machine的材料运输到下一个流程的第2个machine所需要的时间
        '''
        process0.transpotArray = np.array([[46, 51, 14]
                                            [63, 16, 36]
                                            [59, 19, 55]
                                            [23, 76, 73]])
        process1.transpotArray = np.array([[62, 64, 74, 51, 17],
                                            [45, 80, 44, 25, 71],
                                            [48, 28, 47, 73, 29]])
        process2.transpotArray = np.array([[24, 65, 20, 21, 79, 32],
                                            [22, 61, 28, 42, 60, 31],
                                            [54, 37, 60, 16, 27, 44],
                                            [15, 30, 50, 42, 51, 47],
                                            [45, 13, 48, 47, 78, 17]])
        process3.transpotArray = np.array([[64, 27, 79, 12],
                                            [64, 32, 50, 70],
                                            [44, 44, 35, 49],
                                            [57, 45, 62, 53],
                                            [59, 12, 57, 10],
                                            [22, 32, 30, 58]])
        process4.transpotArray = np.array([[41, 13, 59, 25],
                                            [33, 20, 51, 78],
                                            [73, 39, 70, 51],
                                            [53, 52, 45, 59]])
                                    
    
    