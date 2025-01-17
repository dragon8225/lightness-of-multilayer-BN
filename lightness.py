
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab as mpl
from mpl_toolkits.mplot3d import Axes3D

class light:
    def __init__(self, dimension, theta, thick):
        # 初始化
        self.lc = math.pi
        self.dimension = dimension  
        self.layer = int(self.dimension/2) 
        
        self.thick = thick 
        self.theta = theta
        self.z = []
        z = 0
        for i in range(self.layer):
            z = z + self.lc * self.thick[i]
            self.z = self.z + [z]

    def lightness(self):

        
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

        return I[-1] 
        #return I



    