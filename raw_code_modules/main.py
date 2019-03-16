from scipy.interpolate import interp1d
from scipy.integrate import odeint
import csv
from pylab import *


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

def func_v_x(v, t):
	global m
	func = -F_aer_v(v)  / m  + v_wind_h_x(v)
	return func

def func_v_z(v, t):
	global m
	func = -F_aer_v(v)  / m  + v_wind_h_z(v)
	return func

def func_v_h(v, t):
	global m
	func = -F_aer_v(v)  / m - 9.81
	return func

def func_c_x(c, t):
	return f_v_x(t)

def func_c_z(c, t):
	return f_v_z(t)

def func_c_h(c, t):
	return f_v_h(t)


t = linspace(0, 10000, 10000)

v_array_x_raw = odeint(func_v_x, v_0 , t)
v_array_z_raw = odeint(func_v_z, 0 , t)
v_array_h_raw = odeint(func_v_h, 0 , t)

v_array_x = []
for i in v_array_x_raw:
	v_array_x.append(i[0])

v_array_z = []
for i in v_array_z_raw:
	v_array_z.append(i[0])

v_array_h = []
for i in v_array_h_raw:
	v_array_h.append(i[0])

f_v_x = interp1d(t, v_array_x, "nearest", fill_value = "extrapolate")
f_v_z = interp1d(t, v_array_z, "nearest", fill_value = "extrapolate")
f_v_h = interp1d(t, v_array_h, "nearest", fill_value = "extrapolate")


c_array_x_raw = odeint(func_c_x, 0, t)
c_array_z_raw = odeint(func_c_z, 0, t)
c_array_h_raw = odeint(func_c_h, H, t)

c_array_x = []
for i in c_array_x_raw:
	c_array_x.append(i[0])

c_array_z = []
for i in c_array_z_raw:
	c_array_z.append(i[0])

c_array_h = []
for i in c_array_h_raw:
	c_array_h.append(i[0])


# ПОЛУЧЕННЫЕ ФУЕКЦИИ КООРДИНАТ ОТ ВРЕМЕНИ

f_x = interp1d(t, c_array_x, "nearest", fill_value = "extrapolate")
f_z = interp1d(t, c_array_z, "nearest", fill_value = "extrapolate")
f_h = interp1d(t, c_array_h, "nearest", fill_value = "extrapolate")

# ВИЗУАЛИЗАЦИЯ ГРАФИКОВ КООРДИНАТ


