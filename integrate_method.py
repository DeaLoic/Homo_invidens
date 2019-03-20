from scipy.interpolate import interp1d
from scipy.integrate import odeint
from scipy.optimize import fsolve
from matplotlib.pyplot import subplots, plot, show, figure, title, xlabel, ylabel, legend, axes
from matplotlib.pylab import linspace
from math import sqrt
from numpy import array
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


def integral_method(H, v_0, m, v_wind_h_x, v_wind_h_z, f_aer_v,
					samples=100, x_target=0, z_target=0):
	# Записываем систему дифференциальных уравнений в матричном виде, где func(y, x) = dy / dx
	def func(args, t):
		v_x, v_z, v_h, x, z, h = args

		v_air_z = v_z - v_wind_h_z(h)
		v_air_x = v_x - v_wind_h_x(h)
		v_air_full = sqrt(v_air_x ** 2 + v_air_z ** 2 + v_h ** 2)

		f_v_x = - (v_air_x * f_aer_v(v_air_full) / v_air_full) / m
		f_v_z = - (v_air_z * f_aer_v(v_air_full) / v_air_full) / m
		f_v_h = (v_h * f_aer_v(v_air_full) / v_air_full) / m - 9.81
		f_x = v_x
		f_z = v_z
		f_h = v_h
		return [f_v_x, f_v_z, f_v_h, f_x, f_z, f_h]

	# РЕШЕНИЕ ДИФФ УРАВНЕНИЙ

	# Создаем линейное пространство - numpy массив линейно возрастающих чисел - ось аргумента
	t = linspace(0, H, int(samples * H))

	# вызываем функция решения системы дифференциальных уравнений из scipy
	args_t_arrays = odeint(func, [v_0, 0, 0, 0, 0, H], t)

	# создаем дата-фрейм
	trajectory = pd.DataFrame(args_t_arrays, columns=["speed_x", "speed_z", "speed_y", "x", "z", "y"])
	trajectory["t"] = t

	# находим конец траектории (последний y < 0 или первый y > 0)
	i = (trajectory["y"].lt(0).idxmax())

	# для отладки. убрать в конечном(?)
	# if i == 0:
	# 	 i = (trajectory["y"].gt(0).idxmin())

	# отбрасываем ненужную часть
	trajectory = trajectory.loc[0:i, :]

	delta_x = x_target - trajectory.loc[i]["x"]
	delta_z = z_target - trajectory.loc[i]["z"]

	# корректируем траекторию
	trajectory["x"] += delta_x
	trajectory["z"] += delta_z
	trajectory.loc[i]["y"] = 0.0

	return trajectory


if __name__ == "__main__":
	# ЧТЕНИЕ ДАННЫХ И ПОДГОТОВКА МАССИВОВ ДЛЯ РАБОТЫ

	v_0, H = map(int, input("Введите целочисленные v_0, H - через пробелы: ").split())
	m = float(input("input m: "))
	x_target, z_target = map(int, input("Введите x, z целочисленные координаты приземления - через пробелы: ").split())

	wind_csv = pd.read_csv("Wind.csv")
	f_csv = pd.read_csv("F.csv")

	# ФУНКЦИОНАЛЬНЫЙ АНАЛИЗ - ПОДГОТОВКА ДАННЫХ ДЛЯ ДИФФ УРАВНЕНИЙ

	# интерполяция функций
	v_wind_h_x = interp1d(wind_csv["Height (m)"], wind_csv["Wx (m/s)"], "nearest", fill_value="extrapolate")
	v_wind_h_z = interp1d(wind_csv["Height (m)"], wind_csv["Wz (m/s)"], "nearest", fill_value="extrapolate")
	f_aer_v = interp1d(f_csv["V(m/s)"], f_csv["F(N)"], "nearest", fill_value="extrapolate")

	# решение дифф
	trajectory = integral_method(H, v_0, m, v_wind_h_x, v_wind_h_z, f_aer_v)

	'''
	t = linspace(0, H, int(100 * H))
	x_t = interp1d(t, trajectory["x"], "nearest", fill_value="extrapolate")
	z_t = interp1d(t, trajectory["z"], "nearest", fill_value="extrapolate")
	h_t = interp1d(t, trajectory["y"], "nearest", fill_value="extrapolate")
	'''

	figure_2d_coordinates, axe = subplots(num='Координаты от времени')
	title("Графики зависимостей координат от времени")
	xlabel("Время, в секундах")
	ylabel("Координаты, в метрах")
	axe.plot(trajectory["t"], trajectory["x"], color="red")
	axe.plot(trajectory["t"], trajectory["y"], color="blue")
	axe.plot(trajectory["t"], trajectory["z"], color="green")
	legend(("x(t)", "y(t)", "z(t)"))

	# 3d - график - траектория от времени
	figure_3d_trajectory = figure(num='Траектория движения')
	title("Траектория полета тела")
	ax = axes(projection='3d')
	plot(xs=trajectory["x"], zs=trajectory["z"], ys=trajectory["y"], zdir='y')
	ax.set_xlabel('x coordinate, meters')
	ax.set_ylabel('z coordinate, meters')
	ax.set_zlabel('height, [y coordinate], meters')

	show()
