#-*- coding:utf-8 -*-

"""
deep deterministic policy gradient
"""

from itertools import count

import os, random
import numpy as np

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Normal
'''
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default = 'train', type = str) # mode = 'train' or 'test'
parser.add_argument("--env_name", default = "Pendulum-v0") # 游戏名
parser.add_argument('--tau',  default = 0.005, type = float) # target 平滑系数
parser.add_argument('--target_update_interval', default = 1, type = int)
parser.add_argument('--test_iteration', default = 2000, type = int) # 测试时走多少步

parser.add_argument('--learning_rate', default = 1e-3, type = float)
parser.add_argument('--gamma', default = 0.99, type = int) # discounted factor
parser.add_argument('--capacity', default = 50000, type = int) # replay buffer size
parser.add_argument('--batch_size', default = 64, type = int) # mini batch size
parser.add_argument('--seed', default = False, type = bool)
parser.add_argument('--random_seed', default = 9527, type = int)

parser.add_argument('--sample_frequency', default = 256, type = int)
parser.add_argument('--render', default = False, type = bool) # show UI or not, 与下一行配合使用(在训练的时候)
parser.add_argument('--render_interval', default = 300, type = int) # 如果reward大于render_interval, the env.render() will work
parser.add_argument('--log_interval', default = 500, type = int) # 每隔log_interval就保存一次权重
parser.add_argument('--load', default = False, type = bool) # 使用True载入上一次权重并在上一次训练的基础上继续训练
parser.add_argument('--exploration_noise', default = 0.1, type = float)
parser.add_argument('--max_episode', default = 100000, type = int) # 一共运行多少次
parser.add_argument('--max_length_of_trajectory', default = 2000, type = int) # 一次游戏走多少步
parser.add_argument('--print_log', default = 5, type = int) # 每隔print_log就在终端上显示一次
parser.add_argument('--update_iteration', default = 10, type = int)
parser.add_argument('--weight_num', default = 1000, type = int) # 测试时要载入的权重
args = parser.parse_args()

class Replay_buffer():
    def __init__(self, max_size=args.capacity):
        self.storage = []
        self.max_size = max_size
        self.ptr = 0

    def push(self, data):
        if len(self.storage) == self.max_size:
            self.storage[int(self.ptr)] = data
            self.ptr = (self.ptr + 1) % self.max_size
        else:
            self.storage.append(data)

    def sample(self, batch_size):
        ind = np.random.randint(0, len(self.storage), size=batch_size)
        x, y, u, r, d = [], [], [], [], []

        for i in ind:
            X, Y, U, R, D = self.storage[i]
            x.append(np.array(X, copy=False))
            y.append(np.array(Y, copy=False))
            u.append(np.array(U, copy=False))
            r.append(np.array(R, copy=False))
            d.append(np.array(D, copy=False))

        return np.array(x), np.array(y), np.array(u), np.array(r).reshape(-1, 1), np.array(d).reshape(-1, 1)


class Actor(nn.Module):
    def __init__(self, state_dim, action_dim, max_action):
        super(Actor, self).__init__()

        self.l1 = nn.Linear(state_dim, 400)
        self.l2 = nn.Linear(400, 300)
        self.l3 = nn.Linear(300, action_dim)

        self.max_action = max_action

    def forward(self, x):
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = self.max_action * torch.tanh(self.l3(x))
        return x


class Critic(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Critic, self).__init__()

        self.l1 = nn.Linear(state_dim + action_dim, 400)
        self.l2 = nn.Linear(400 , 300)
        self.l3 = nn.Linear(300, 1)

    def forward(self, x, u):
        x = F.relu(self.l1(torch.cat([x, u], 1)))
        x = F.relu(self.l2(x))
        x = self.l3(x)
        return x


class DDPG(object):
    def __init__(self, state_dim, action_dim, max_action):
        self.actor = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_target = Actor(state_dim, action_dim, max_action).to(device)
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = optim.Adam(self.actor.parameters(), args.learning_rate)

        self.critic = Critic(state_dim, action_dim).to(device)
        self.critic_target = Critic(state_dim, action_dim).to(device)
        self.critic_target.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = optim.Adam(self.critic.parameters(), args.learning_rate)
        self.replay_buffer = Replay_buffer()
        self.num_critic_update_iteration = 0
        self.num_actor_update_iteration = 0
        self.num_training = 0

    def select_action(self, state):
        # FloatTensor 建立FloatTensor类型
        state = torch.FloatTensor(state.reshape(1, -1)).to(device)
        # cpu():提取CPU的data数据, numpy():tensor转numpy, flatten():降成一维
        return self.actor(state).cpu().data.numpy().flatten()

    def update(self):
        for it in range(args.update_iteration):
            # Sample replay buffer
            x, y, u, r, d = self.replay_buffer.sample(args.batch_size)
            state = torch.FloatTensor(x).to(device)
            action = torch.FloatTensor(u).to(device)
            next_state = torch.FloatTensor(y).to(device)
            done = torch.FloatTensor(d).to(device)
            reward = torch.FloatTensor(r).to(device)

            # Compute the target Q value
            target_Q = self.critic_target(next_state, self.actor_target(next_state))
            target_Q = reward + ((1 - done) * args.gamma * target_Q).detach()

            # Get current Q estimate
            current_Q = self.critic(state, action)

            # Compute critic loss
            critic_loss = F.mse_loss(current_Q, target_Q)
            
            # Optimize the critic
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            self.critic_optimizer.step()

            # Compute actor loss
            actor_loss = -self.critic(state, self.actor(state)).mean()

            # Optimize the actor
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

            # Update the frozen target models
            for param, target_param in zip(self.critic.parameters(), self.critic_target.parameters()):
                target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)

            for param, target_param in zip(self.actor.parameters(), self.actor_target.parameters()):
                target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)

            self.num_actor_update_iteration += 1
            self.num_critic_update_iteration += 1
            

    def save(self, i):
        torch.save(self.actor.state_dict(), directory + str(i) + '_actor.pth')
        torch.save(self.critic.state_dict(), directory + str(i) + '_critic.pth')
        print("====================================")
        print("Model has been saved...")
        print("====================================")

    def load(self, i):
        self.actor.load_state_dict(torch.load(directory + str(i) + '_actor.pth'))
        self.critic.load_state_dict(torch.load(directory + str(i) + '_critic.pth'))
        print("====================================")
        print("model has been loaded...")
        print("====================================")
    
'''
# use the cuda
device = 'cuda' if torch.cuda.is_available() else 'cpu'
if device == 'cuda':
    print('using the GPU...')

script_name = os.path.basename(__file__) # return the name of this script
env = gym.make('Pendulum-v0').unwrapped
'''
if args.seed:
    env.seed(args.random_seed)
    torch.manual_seed(args.random_seed)
    np.random.seed(args.random_seed)
'''
state_dim = env.observation_space.shape[0]
print(state_dim)
action_dim = env.action_space.shape[0]
print(action_dim)
max_action = float(env.action_space.high[0])
print(max_action)
min_Val = torch.tensor(1e-7).float().to(device) # min value
print(min_Val)
'''
# maybe you want to modify the directory to save
directory = './exp_ddpg_' + args.env_name +'./'

def main(agent):
    ep_r = 0
    
    # test
    if args.mode == 'test':
        agent.load(args.weight_num)
        for i in range(args.test_iteration):
            state = env.reset()
            for t in count():
                action = agent.select_action(state)
                next_state, reward, done, info = env.step(np.float32(action))
                ep_r += reward
                env.render()
                if done or t >= args.max_length_of_trajectory:
                    print("Ep_i {:>10d}, the ep_r is {:>15.2f}, the step is {:>10d}".format(i, ep_r, t))
                    ep_r = 0
                    break
                state = next_state
                
    # train
    elif args.mode == 'train':
        print("====================================")
        print("Collection Experience...")
        print("====================================")
        if args.load:
            # 要载入的权重
            agent.load(args.weight_num)
            print('load model...')
        for i in range(args.max_episode):
            # 环境回归原位
            state = env.reset()
            for t in count():
                action = agent.select_action(state)

                # issue 3 add noise to action
                action = (action + np.random.normal(0, args.exploration_noise, size=env.action_space.shape[0])).clip(
                    env.action_space.low, env.action_space.high)

                next_state, reward, done, info = env.step(action)
                ep_r += reward
                # 权重小于render_interval时显示, render是bool类型, ep_r是负数, args.render_interval是正数, 所以ep_r取绝对值
                if args.render == 1 and abs(ep_r) <= args.render_interval :
                    env.render()
                agent.replay_buffer.push((state, next_state, action, reward, np.float(done)))

                state = next_state
                if done or t >= args.max_length_of_trajectory:
                    # 第一个参数是图表名, 第二个参数是纵坐标, 第三个参数是横坐标
                    #agent.writer.add_scalar('ep_r', ep_r, global_step=i)
                    if i % args.print_log == 0:
                        print("Ep_i {:>10d}, the ep_r is {:>15.2f}, the step is {:>10d}".format(i, ep_r, t))
                    ep_r = 0
                    break

            if i % args.log_interval == 0 and i != 0:
                agent.save(i)
                
            if len(agent.replay_buffer.storage) >= args.capacity-1:
                agent.update()
            
    else:
        raise NameError("mode wrong!!!")
'''
'''
查看tensorboard: 中终端输入绝对路径, eg:
tensorboard --logdir D:\MyNetWork\DDPG_Pytorch\exp_ddpg_Pendulum-v0
'''
if __name__ == '__main__':
    agent = DDPG(state_dim, action_dim, max_action)
    main(agent)
