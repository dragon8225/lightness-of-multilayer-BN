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
    

    theta_low = []
    theta_up = []
    t_low = []
    t_up = []
    for i in range(layer):
        theta_low = theta_low + [theta_min]
        theta_up = theta_up + [theta_max]
        t_low = t_low + [t_min]
        t_up = t_up + [t_max]

    low = theta_low + t_low
    up = theta_up + t_up

    g_o = GO(dimension, thick, low, up)
    Imax, theta, t = g_o.glo()
    print('lightness：{} angle：{}  thickness_per_layer：{}'.format(Imax, theta, t))

