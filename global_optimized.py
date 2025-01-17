# -*- coding: utf-8 -*-

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import pylab as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']

"""find global optimized value
dimension：layers * 2
thickness：thickness
time、size、vlow、vhigh：parameters
"""
class GO:
    def __init__(self, dimension, thickness, low, up, time = 250, size = 150, v_low = -0.02, v_high= 0.02):
        #PSO
        self.lc = math.pi
        self.dimension = dimension  
        self.layer = int(self.dimension/2) 
        self.thickness = thickness * self.lc 
        self.time = time  
        self.size = size  
        self.low = low
        self.up = up
        self.bound = []  
        self.bound.append(low)
        self.bound.append(up)
        self.v_low = v_low
        self.v_high = v_high
        self.x = np.zeros((self.size, self.dimension))  
        self.v = np.zeros((self.size, self.dimension))  
        self.p_best = np.zeros((self.size, self.dimension))  
        self.g_best = np.zeros((1, self.dimension))[0]  

        temp = -1000000
        for i in range(self.size):
            for j in range(self.layer):
                self.x[i][j] = random.uniform(self.bound[0][j], self.bound[1][j])
                self.x[i][j + self.layer] = random.uniform(self.bound[0][j + self.layer], self.bound[1][j + self.layer])
                self.x[i][0] = 0 
                self.v[i][j] = random.uniform(self.v_low, self.v_high)
            self.p_best[i] = self.x[i]  
            fit = self.lightness(self.p_best[i])
            
            if fit > temp:
                self.g_best = self.p_best[i]
                temp = fit

    def lightness(self, x):
        """
        calculate the lightness
        """
        theta_a = np.zeros(self.layer)
        z_a = np.zeros(self.layer)
        Sum = sum(x[self.layer: self.dimension])
        z_a[0] = self.thickness * x[0 + self.layer]/Sum
        for i in range(1, self.layer):
            theta_a[i] = x[i]
            z_a[i] = self.thickness * x[i + self.layer]/Sum + z_a[i - 1]
        ans1_a = math.cos(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))
        ans2_a = math.sin(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))
        for i in range(1, self.layer):
            ans1_a = ans1_a + math.cos(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))
            ans2_a = ans2_a + math.sin(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))
        ans = np.abs(ans1_a) ** 2 + np.abs(ans2_a) ** 2

        return ans

    def update(self, size):
        c1 = 2.0  
        c2 = 2.0
        w = 0.8  
        for i in range(size):
            
            self.v[i] = w * self.v[i] + c1 * random.uniform(0, 1) * (
                    self.p_best[i] - self.x[i]) + c2 * random.uniform(0, 1) * (self.g_best - self.x[i])
            
            for j in range(self.dimension):
                if self.v[i][j] < self.v_low:
                    self.v[i][j] = self.v_low
                if self.v[i][j] > self.v_high:
                    self.v[i][j] = self.v_high

            
            self.x[i] = self.x[i] + self.v[i]
            self.x[i][0] = 0
            
            for j in range(self.dimension):
                if self.x[i][j] < self.bound[0][j]:
                    self.x[i][j] = self.bound[0][j]
                if self.x[i][j] > self.bound[1][j]:
                    self.x[i][j] = self.bound[1][j]
            
            if self.lightness(self.x[i]) > self.lightness(self.p_best[i]):
                self.p_best[i] = self.x[i]
            if self.lightness(self.x[i]) > self.lightness(self.g_best):
                self.g_best = self.x[i]

    def glo(self):
        best = []
        
        self.final_best_theta = np.random.random(self.layer) * 1 * self.up[0:self.layer]
        self.final_best_theta[0] = 0
        self.final_best_z = np.random.random(self.layer)
        self.final_best = np.append(self.final_best_theta, self.final_best_z)
        for gen in range(self.time):
            self.update(self.size)
            if self.lightness(self.g_best) > self.lightness(self.final_best):
                self.final_best = self.g_best.copy()
            
            temp = self.lightness(self.final_best)
            
            best.append(temp)
        t = [i for i in range(self.time)]
        self.final_best_theta = self.final_best[0:self.layer]
        self.final_best_z = self.final_best[self.layer:self.dimension]
        self.final_best_z = self.final_best_z/self.final_best_z.sum() * self.thickness/self.lc


        return best[-1], self.final_best_theta, self.final_best_z

