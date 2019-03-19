import pandas as pd
from scipy.interpolate import interp1d

F_from_V = pd.read_csv('F.csv', sep = ',')
Wind = pd.read_csv('Wind.csv', ser = ',')

F_from_V = interp1d(F_from_V['V(m/s)'], F_from_V['F(N)'])
Wind_x = interp1d(Wind['Height (m)'], Wind['Wx (m/s)'])
Wind_x = interp1d(Wind['Height (m)'], Wind['Wz (m/s)'])

m, H, V_start, x_aim, z_aim = map(float, input('Введите массу груза, высоту сброса, скорость груза при сбросе, x и z координаты точки попадания:').split())
