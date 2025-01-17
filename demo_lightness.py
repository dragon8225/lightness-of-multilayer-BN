##
from lightness import light


if __name__ == '__main__':
    
    
    layer = 4
    dimension = 2 * layer 

    theta = [0., 0., 0., 0.]

    thick = [0.4, 0.4, 0.4, 0.4]

    light1 = light(dimension, theta, thick)
    I = light1.lightness()
    print(I)
    