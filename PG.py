#-*- coding:utf-8 -*-

"""
policy Gradient
"""

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# 定义全连接神经网络
class Net(nn.Module):
    # 搭建网络, state_dim 状态个数, hidden_dim 隐藏层个数, action_dim 动作个数
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(Net, self).__init__()

        self.l1 = nn.Linear(state_dim, hidden_dim)
        self.l2 = nn.Linear(hidden_dim, action_dim)

    # 前向传播
    def forward(self, x):
        # 各个元素调用relu函数, 为了增加非线性性
        x = F.relu(self.l1(x))
        action_scores = self.l2(x)
        # 对张量用softmax函数, 得到是0-1之间的值
        return F.softmax(action_scores)


class PolicyGradient:
    def __init__(self, state_dim, hidden_dim, action_dim):
        # 实例化神经网络 to(device)决定使用GPU或者CPU, 实例化时会定义
        self.model = Net(state_dim, hidden_dim, action_dim).to(device)
        # optimizer:优化器, lr:learning_rate
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        
    # 选择动作
    def select_action(self, state):
        probs = self.model(Variable(state).to(device))
        action = probs.multinomial().data
        prob = probs[:, action[0,0]].view(1, -1)
        log_prob = prob.log()
        entropy = - (probs*probs.log()).sum()

        return action[0], log_prob, entropy
    
    # 更新
    def update(self, rewards, log_probs, entropies, gamma):
        # R = 0 tensor类型 一行一列
        R = torch.zeros(1, 1)
        loss = 0
        for i in reversed(range(len(rewards))):
            R = gamma * R + rewards[i]
            loss = loss - (log_probs[i]*(Variable(R).expand_as(log_probs[i])).to(device)).sum() - (0.0001*entropies[i].to(device)).sum()
        loss = loss / len(rewards)
        
        # 优化网络
        self.optimizer.zero_grad()
        loss.backward()
        # 梯度剪切, 防止梯度消失
        #nn.utils.clip_grad_norm(self.model.parameters(), 40)
        self.optimizer.step()
        
    def save(self, i):
        torch.save(self.model.state_dict(), directory + str(i) + '.pth')
        print("====================================")
        print("Model has been saved...")
        print("====================================")
    
    def load(self, i):
        self.model.load_state_dict(torch.load(directory + str(i) + '.pth'))
        print("====================================")
        print("model has been loaded...")
        print("====================================")
    
