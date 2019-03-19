import pandas as pd
from scipy.interpolate import interp1d

def step(H, eps):
    return 0.01

F_from_V = pd.read_csv('F.csv', sep = ',')
Wind = pd.read_csv('Wind.csv', sep = ',')

F_from_V = interp1d(F_from_V['V(m/s)'], F_from_V['F(N)'])
Wind_x = interp1d(Wind['Height (m)'], Wind['Wx (m/s)'])
Wind_z = interp1d(Wind['Height (m)'], Wind['Wz (m/s)'])

m, H, V_start, x_aim, z_aim, eps = map(float, input('Введите массу груза,\
высоту сброса, скорость груза при сбросе, x и z координаты точки попадания\
и требуемую точность попадания:').split())

g = 9.8

delta_t = step(H, eps)
