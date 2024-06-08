from global_optimized import GO
import math

if __name__ == '__main__':
    layer = 5
    dimension = layer * 2
    thick = layer * 0.4
    theta_min = 0
    theta_max = math.pi 
    t_min = 0.4
    t_max = 0.4
    
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

    g_o = GO(dimension, thick, low, up)
    Imax, theta, t = g_o.glo()
    print('光强：{} 每层角度：{}  每层厚度：{}'.format(Imax, theta, t))