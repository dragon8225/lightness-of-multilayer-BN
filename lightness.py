"""给定每层厚度和角度后求光强"""
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab as mpl
from mpl_toolkits.mplot3d import Axes3D

"theta和thick是角度和厚度的列表"
class light:
    def __init__(self, dimension, theta, thick):
        # 初始化
        self.lc = math.pi
        self.dimension = dimension  # 变量个数
        self.layer = int(self.dimension/2) #层数
        
        self.thick = thick #单位为lc
        self.theta = theta
        self.z = []#转化为每一层的z坐标列表
        z = 0
        for i in range(self.layer):
            z = z + self.lc * self.thick[i]
            self.z = self.z + [z]
        #print(np.array(self.z)/math.pi)
    def lightness(self):
        """
        光强计算 Ex是二次谐波电场x方向场强，Ey是二次谐波电场y方向场强，I是总光强
        """
        theta_a = self.theta
        z_a = self.z
        Ex = np.zeros(self.layer, dtype=complex)
        Ey = np.zeros(self.layer, dtype=complex)
        I = np.zeros(self.layer)
        
        Ex[0] = math.cos(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))
        Ey[0] = math.sin(3 * 0)*(1 - np.exp(- 1j * 1 * z_a[0]))

        I [0] = np.abs(Ex[0])**2 + np.abs(Ey[0])**2

        for i in range(1, self.layer):
            Ex[i] = Ex[i - 1 ] + math.cos(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))
            Ey[i] = Ey[i - 1 ] + math.sin(3 * theta_a[i])*(np.exp(- 1j * 1 * z_a[i-1]) - np.exp(- 1j * 1 * z_a[i]))
            
            I[i] = np.abs(Ex[i]) ** 2 + np.abs(Ey[i]) ** 2

        return I[-1] #输出最后的光强，如果想要每一层的光强，返回I就行#
        #return I


##
if __name__ == '__main__':
    
    
    layer = 4
    dimension = 2 * layer #变量个数
    #弧度制角度#
    theta = [0., 0., 0., 0.]
    #单位为lc的厚度#
    thick = [0.4, 0.4, 0.4, 0.4]

    light1 = light(dimension, theta, thick)
    I = light1.lightness()
    print(I)
    
    