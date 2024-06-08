import numpy as np
import math

#输入总厚度，单位为lc#
thick = 3.5
Iquasi = np.abs(2 * int(thick) + 1 - np.exp(-1j * math.pi * (thick - int(thick))))**2