# Reinforce-learning based algorithm for dynamic scheduling problem in steelmaking workshop
基于强化学习的炼钢动态调度求解技术和软件实现
------

## 文件说明
### model文件夹
model文件夹储存各种算法:  
> * `PG.py`: policy Gradient 算法  
> * `PGtest.py`: policy Gradient 算法测试, 测试对象 openAI CartPole-v0  
> * `DDPG.py`: deep deterministic policy gradient 算法  
> * `DDPGtets.py`: deep deterministic policy gradient 算法测试  
> * `DDDPG.py`: deep deterministic discrete policy gradient 算法  

### 调度系统
`background.py`: 定义调度系统的流程数量, 工艺种类等各种信息  
`agents.py`: 分布式多agent集群  
`environment.py`: 整个项目的环境  
`utils.py`: 自定义工具包  
`test.py`: 测试运行, 随机算法运行, 测试系统的可用性  
`ui.py`: 运行则会显示ui界面  
`train.py`: 神经网络训练, 算法DDDPG  