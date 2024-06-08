# -*- coding: utf-8 -*-

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pylab as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

"""寻找全局最优解
核心类global optimized：
dimension：层数*2，即每层的theta和t
thickness：总厚度
time、size、vlow、vhigh：迭代参数
low、up：theta和t的上下限，为方便操作把theta列表和t列表合成一个，theta在前t在后"""
class GO:
    def __init__(self, dimension, thickness, low, up, time = 250, size = 150, v_low = -0.02, v_high= 0.02):
        # 初始化
        self.lc = math.pi
        self.dimension = dimension  # 变量个数
        self.layer = int(self.dimension/2) #层数
        self.thickness = thickness * self.lc #总厚度
        self.time = time  # 迭代的代数
        self.size = size  # 种群大小
        self.low = low
        self.up = up
        self.bound = []  # 变量的约束范围
        self.bound.append(low)
        self.bound.append(up)
        self.v_low = v_low
        self.v_high = v_high
        self.x = np.zeros((self.size, self.dimension))  # 所有粒子的位置
        self.v = np.zeros((self.size, self.dimension))  # 所有粒子的速度
        self.p_best = np.zeros((self.size, self.dimension))  # 每个粒子最优的位置
        self.g_best = np.zeros((1, self.dimension))[0]  # 全局最优的位置

        # 初始化第0代初始全局最优解
        temp = -1000000
        for i in range(self.size):
            for j in range(self.layer):
                self.x[i][j] = random.uniform(self.bound[0][j], self.bound[1][j])
                self.x[i][j + self.layer] = random.uniform(self.bound[0][j + self.layer], self.bound[1][j + self.layer])
                self.x[i][0] = 0 #角度设定为0#
                self.v[i][j] = random.uniform(self.v_low, self.v_high)
            self.p_best[i] = self.x[i]  # 储存最优的个体
            fit = self.lightness(self.p_best[i])
            # 做出修改
            if fit > temp:
                self.g_best = self.p_best[i]
                temp = fit

    def lightness(self, x):
        """
        光强计算
        """
        theta_a = np.zeros(self.layer)
        z_a = np.zeros(self.layer)
        Sum = sum(x[self.layer: self.dimension])
        z_a[0] = self.thickness * x[0 + self.layer]/Sum
        for i in range(1, self.layer):
            theta_a[i] = x[i]
            z_a[i] = self.thickness * x[i + self.layer]/Sum + z_a[i - 1]
        ans1_a = math.cos(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))#第一层x方向二次谐波场强y
        ans2_a = math.sin(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))#第一层y方向二次谐波场强
        for i in range(1, self.layer):
            ans1_a = ans1_a + math.cos(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))#x方向二次谐波场强
            ans2_a = ans2_a + math.sin(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))#y方向二次谐波场强
        ans = np.abs(ans1_a) ** 2 + np.abs(ans2_a) ** 2

        return ans

    def update(self, size):
        c1 = 2.0  # 学习因子
        c2 = 2.0
        w = 0.8  # 自身权重因子
        for i in range(size):
            # 更新速度(核心公式)
            self.v[i] = w * self.v[i] + c1 * random.uniform(0, 1) * (
                    self.p_best[i] - self.x[i]) + c2 * random.uniform(0, 1) * (self.g_best - self.x[i])
            # 速度限制
            for j in range(self.dimension):
                if self.v[i][j] < self.v_low:
                    self.v[i][j] = self.v_low
                if self.v[i][j] > self.v_high:
                    self.v[i][j] = self.v_high

            # 更新位置
            self.x[i] = self.x[i] + self.v[i]
            self.x[i][0] = 0
            # 位置限制
            for j in range(self.dimension):
                if self.x[i][j] < self.bound[0][j]:
                    self.x[i][j] = self.bound[0][j]
                if self.x[i][j] > self.bound[1][j]:
                    self.x[i][j] = self.bound[1][j]
            # 更新p_best和g_best
            if self.lightness(self.x[i]) > self.lightness(self.p_best[i]):
                self.p_best[i] = self.x[i]
            if self.lightness(self.x[i]) > self.lightness(self.g_best):
                self.g_best = self.x[i]

    def glo(self):
        best = []
        #设定一个可能最大的地方#
        self.final_best_theta = np.random.random(self.layer) * 1 * self.up[0:self.layer]
        self.final_best_theta[0] = 0
        self.final_best_z = np.random.random(self.layer)
        self.final_best = np.append(self.final_best_theta, self.final_best_z)
        for gen in range(self.time):
            self.update(self.size)
            if self.lightness(self.g_best) > self.lightness(self.final_best):
                self.final_best = self.g_best.copy()
            #print('每层角度：{}  每层厚度：{}'.format(self.final_best[:self.layer], self.final_best[self.layer : self.dimension] * self.thickness/sum(self.final_best[self.layer: self.dimension])))
            temp = self.lightness(self.final_best)
            #print('光强：{}'.format(temp))
            best.append(temp)
        t = [i for i in range(self.time)]
        self.final_best_theta = self.final_best[0:self.layer]
        self.final_best_z = self.final_best[self.layer:self.dimension]
        self.final_best_z = self.final_best_z/self.final_best_z.sum() * self.thickness/self.lc
        #print(self.final_best_z.sum())
        
        #下方代码为迭代是否收敛的图像

        # plt.figure()
        # plt.grid(axis='both')
        # plt.plot(t, best, color='red', marker='.', ms=10)
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.margins(0)
        # plt.xlabel(u"迭代次数")  # X轴标签
        # plt.ylabel(u"光强")  # Y轴标签
        # plt.title(u"迭代过程")  # 标题
        # plt.show()

        return best[-1], self.final_best_theta, self.final_best_z

if __name__ == '__main__':
    
    # #单次
    # pso = PSO(dimension, thickness, time, size, low, up, v_low, v_high)
    # Imax, theta, z = pso.pso()
    # print('光强：{} 每层角度：{}  每层厚度：{}'.format(Imax, theta, z))

    #扫一下固定层数，总厚度变化的情况
    "迭代参数（可不修改）"
    time = 250 #迭代参数
    size = 150 #迭代参数
    v_low = -0.02#寻找速度
    v_high = 0.02

    "基础参数"
    layer = 20
    dimension = 2 * layer #变量个数 
    #thickness = 1 #总厚度为thickness*lc
    lc = math.pi
    
    "总厚度遍历模块"
    points = 30 #厚度遍历的点数#
    thickness_min = 0 #单位为lc#
    thickness_max = 4
    thickness = np.linspace(thickness_min, thickness_max, points)
    
    "每层转角与厚度的限制模块"
    #设置每层转角和厚度theta和t寻找的上下限，t的单位为lc
    theta_min = 0
    theta_max = math.pi 
    t_min = 0
    t_max = 1
    
    #此处也可以单独设置每一层寻找的角度和厚度范围
    theta_low = []
    theta_up = []
    t_low = []
    t_up = []
    for i in range(layer):
        theta_low = theta_low + [theta_min]
        theta_up = theta_up + [theta_max]
        t_low = t_low + [t_min]
        t_up = t_up + [t_max]
    #合到一个列表里
    low = theta_low + t_low
    up = theta_up + t_up

    "输出数据"
    #输出的三种数据，最大光强、转角、层厚
    Imax = np.zeros(points)#全局最优
    theta = np.zeros([points, layer])
    t = np.zeros([points, layer])
    #Iquasi = np.zeros(points)#准相位匹配
    for i in range(points):
        thick = thickness[i]
        g_o = GO(dimension, thick, low, up, time, size, v_low, v_high)
        Imax[i], theta[i], t[i] = g_o.glo()
        print('光强：{} 每层角度：{}  每层厚度：{}'.format(Imax[i], theta[i], t[i]))
        #Iquasi[i] = np.abs(2 * int(thick) + 1 - np.exp(-1j * math.pi * (thick - int(thick))))**2

    np.save('globaldata/Imax.npy', Imax)
    np.save('globaldata/thickness.npy', thickness)
    np.save('globaldata/theta.npy', theta)
    np.save('globaldata/t.npy', t)
    # plt.plot(thickness, Imax, label = 'max')
    # plt.plot(thickness, Iquasi, label = 'quasi')
    # plt.plot(thickness, (thickness * lc) ** 2, label = 'perfect')
    # plt.legend()
    
    # plt.show()  
     