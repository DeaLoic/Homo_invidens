from scipy.interpolate import interp1d
from scipy.integrate import odeint
import csv
from pylab import *
import matplotlib.pyplot as plt


# ЧТЕНИЕ ДАННЫХ И ПОДГОТОВКА МАССИВОВ ДЛЯ РАБОТЫ

v_0, H, m = map(int, input("Введите v_0, H, m - через пробелы: ").split())

reader_wind = csv.reader(open("Wind.csv", "r"))
reader_F = csv.reader(open("F.csv", "r"))

F_sequence = [] 
v_sequence = []
v_wind_sequence_x = []
v_wind_sequence_z = []
h_sequence = []

trigger = 1
for line in reader_F:
	if trigger:
		trigger = 0
	else:
		v_sequence.append(float(line[0]))
		F_sequence.append(float(line[1]))

trigger = 1
for line in reader_wind:
	if trigger:
		trigger = 0
	else:
		h_sequence.append(float(line[0]))
		v_wind_sequence_x.append(float(line[1]))
		v_wind_sequence_z.append(float(line[1]))



# ФУНКЦИОНАЛЬНЫЙ АНАЛИЗ - ПОДГОТОВКА ДАННЫХ ДЛЯ ДИФФ УРАВНЕНИЙ

# интерполяция функций
v_wind_h_x = interp1d(h_sequence, v_wind_sequence_x, "nearest", fill_value = "extrapolate")
v_wind_h_z = interp1d(h_sequence, v_wind_sequence_z, "nearest", fill_value = "extrapolate")
F_aer_v = interp1d(v_sequence, F_sequence, "nearest", fill_value = "extrapolate")


# РЕШЕНИЕ ДИФФ УРАВНЕНИЙ

t = linspace(0, H, H)

def func(args, t):

	global m

	v_x, v_z, v_h, x, z, h = args

	f_v_x = -F_aer_v(v_x)  / m  + v_wind_h_x(h) 
	f_v_z = -F_aer_v(v_z)  / m  + v_wind_h_z(h)
	f_v_h = -F_aer_v(v_h)  / m + 9.81
	f_x = v_x
	f_z = v_z
	f_h = v_h

	return [f_v_x, f_v_z, f_v_h, f_x, f_z, f_h]

args_t_arrays = odeint(func, [v_0, 0, 0, 0, 0, H], t)

vx_t_array = args_t_arrays[:, 0]
vz_t_array = args_t_arrays[:, 1]
vh_t_array = args_t_arrays[:, 2]
x_t_array = args_t_arrays[:, 3]
z_t_array = args_t_arrays[:, 4]
h_t_array = args_t_arrays[:, 5]

# ВИЗУАЛИЗАЦИЯ И ВСЕ ДЕЛА

_, axe = plt.subplots()
axe.plot(x_t_array, t, color = "red")
axe.plot(z_t_array, t, color = "green")
axe.plot(h_t_array, t, color = "blue")

plt.show()