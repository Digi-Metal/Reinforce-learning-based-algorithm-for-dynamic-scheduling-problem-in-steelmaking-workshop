#-*- coding:utf-8 -*-

"""
ui.py
pyqtgraph-0.10.0版

可视化ui界面
"""

from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import sys

'''
辅助函数, 根据state返回甘特图的框的位置
输入设备的位置: 流程号和设备号
返回对应的甘特图框的坐标, list格式
'''
def gantPosition(process, num):
    ls = [[26, 25, 24, 23],
          [22, 21, 20, 19, 18, 17],
          [16, 15, 14, 13, 12],
          [11, 10,  9],
          [ 8,  7,  6,  5],
          [ 4,  3,  2,  1]]
    return ls[process][num]

'''
甘特图中的框的类
输入一条数据,list类型, 输出是数据对应甘特图的框
继承于pyqtgraph的GraphicsObject类
'''
class BarItem(pg.GraphicsObject):
    def __init__(self, states, times):
        self.gant_wide = 0.2 # 甘特图的框的宽度的一半
        self.states = states
        self.times = times
        pg.GraphicsObject.__init__(self)
        self.generatePicture() # 实例化时即调用
    
    # 根据states数据画框
    def generatePicture(self):
        states = self.states
        times = self.times
        self.picture = QtGui.QPicture() # 实例化一个绘图设备
        p = QtGui.QPainter(self.picture) # 在picture上实例化QPainter用于绘图
        
        machineStates = states[1:]
        # 遍历每一个设备, 判断并画框或划线, 损坏,空闲
        for eachprocess in range(len(machineStates)):
            for each in range(len(machineStates[eachprocess])):
                data = machineStates[eachprocess][each] # 获取设备的状态
                # 设备在运行job时, 画框
                if data[0] == 1:
                    # 选颜色, task1为红, task2为黄, task1为绿
                    if data[1] == 1:
                        p.setPen(pg.mkPen('r'))
                        p.setBrush(pg.mkBrush('r')) # 设置画刷颜色为红
                    elif data[1] == 2:
                        p.setPen(pg.mkPen('g'))
                        p.setBrush(pg.mkBrush('g')) # 设置画刷颜色为绿
                    elif data[1] == 3:
                        p.setPen(pg.mkPen('y'))
                        p.setBrush(pg.mkBrush('y')) # 设置画刷颜色为黄
                    # 绘制箱子,格式:(a,b,c,d)为左下角xy坐标,向xy轴正方向占多少距离
                    coord_left = gantPosition(eachprocess, each)
                    p.drawRect(QtCore.QRectF(times,coord_left-self.gant_wide,1,2*self.gant_wide))
                # job占用在设备时, 画白框
                elif data[0] == 3:
                    p.setPen(pg.mkPen('b'))
                    p.setBrush(pg.mkBrush('b'))
                    coord_left = gantPosition(eachprocess, each)
                    p.drawRect(QtCore.QRectF(times,coord_left-self.gant_wide,1,2*self.gant_wide))
        p.end()
        
    # 不用管这个, 这个函数是pg.GraphicsObject类有关的
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
        
    # # 不用管这个, 这个函数是pg.GraphicsObject类有关的
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


# 主窗口类
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 添加主窗口
        self.setWindowTitle("在线调度系统 0.0.1版") # 设置窗口标题
        self.main_widget = QtWidgets.QWidget() # 实例化一个主部件
        self.main_layout = QtWidgets.QGridLayout() # 实例化一个网格布局层
        self.main_widget.setLayout(self.main_layout) # 设置主部件布局为网格布局
        self.setCentralWidget(self.main_widget) # 设置窗口默认部件为主部件
        
        # 添加主窗口的按钮,下拉框,文本输入框等部件
        self.stock_code = QtWidgets.QLineEdit() # 创建一个文本输入框部件
        self.option_sel = QtWidgets.QComboBox() # 创建一个下拉框部件
        self.option_sel.addItem("甘特图") # 增加下拉框选项
        self.option_sel.addItem("设备状态")
        self.que_btn = QtWidgets.QPushButton("运行") # 创建一个按钮部件
        
        # 创建空白图形,用于放置甘特图
        pg.setConfigOption('background', 'w') # 背景为白
        self.gant_widget = QtWidgets.QWidget() # 实例化widget部件作为甘特图部件
        self.gant_layout = QtWidgets.QGridLayout()
        self.gant_widget.setLayout(self.gant_layout)
        self.gant_plt = pg.PlotWidget() # 实例化一个绘图部件
        self.gant_layout.addWidget(self.gant_plt) # 添加绘图部件到网格布局层
        
        # 设置部件的布局位置,格式(部件,a,b,c,d):添加到第a行第b列，占c行占d列
        self.main_layout.addWidget(self.stock_code,0,0,1,1)
        self.main_layout.addWidget(self.option_sel,0,1,1,1)
        self.main_layout.addWidget(self.que_btn,0,2,1,1)
        self.main_layout.addWidget(self.gant_widget,1,0,3,3)

    # 画一个t时刻的state的甘特图
    def plotGantGraph(self, states, times):
        item = BarItem(states, times)
        self.gant_plt.addItem(item, )  # 在绘图部件中添加甘特图项目
        self.gant_plt.showGrid(x=True, y=True)  # 设置绘图部件显示网格线
        self.gant_plt.setYRange(max=26,min=0)
        self.gant_plt.setLabel(axis='left', text='设备')  # 设置Y轴标签
        self.gant_plt.setLabel(axis='bottom', text='运行时间')  # 设置X轴标签


# 获取数据, 显示ui
def main():
    # 修改需要显示的文件名
    filename = "record_2020_04_12_00_37_54"
    
    # 读取文件
    ls = []
    with open("record/" + filename + "/state_record.txt") as f:
        for eachLine in f:
            ls.append(eval(eachLine))
    
    # 画图
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    for each in range(len(ls)):
        gui.plotGantGraph(ls[each], each)
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

'''
# 待改进: 
Y轴要把数字换成设备号, 可以考虑隐藏y轴
坐标轴分度值
运输部分没有连线
看看能不能搞个x轴拖动条

# 在运输job时, 画线
elif data[0] == 2 and data[-1] == 1:
    if data[1] == 1:
        p.setPen(pg.mkPen('r'))
    elif data[1] == 2:
        p.setPen(pg.mkPen('g'))
    elif data[1] == 3:
        p.setPen(pg.mkPen('y'))
    coord_left = gantPosition(eachprocess, data[2])
    coord_right = gantPosition(eachprocess+1, data[3])
    p.drawLine(QtCore.QPointF(1, coord_left), QtCore.QPointF(3, coord_right)).....
'''
