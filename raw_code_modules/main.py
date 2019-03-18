from scipy.interpolate import interp1d
from scipy.integrate import odeint
from matplotlib.pyplot import subplots, plot, show, figure, title, xlabel, ylabel, legend, axes
from matplotlib.pylab import linspace
from pynverse import inversefunc
from csv import reader
from math import ceil
from numpy import array
from mpl_toolkits.mplot3d import Axes3D


# ЧТЕНИЕ ДАННЫХ И ПОДГОТОВКА МАССИВОВ ДЛЯ РАБОТЫ

v_0, H, m = map(int, input("Введите целочисленные v_0, H, m - через пробелы: ").split())
x_target, z_target = map(int, input("Введите x, z целочисленные координаты приземления - через пробелы: ").split())

reader_wind = reader(open("Wind.csv", "r"))
reader_F = reader(open("F.csv", "r"))

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

# Создаем линейное пространство - numpy массив линейно возрастающих чисел - ось аргумента
t = linspace(0, 10*H, 100*H)

# Записываем систему дифференциальных уравнений в матричном виде, где func(y, x) = dy / dx
def func(args, t):

	global m

	v_x, v_z, v_h, x, z, h = args

	f_v_x = F_aer_v(v_x)  / m  + v_wind_h_x(h) 
	f_v_z = F_aer_v(v_z)  / m  + v_wind_h_z(h)
	f_v_h = F_aer_v(v_h)  / m - 9.81
	f_x = v_x
	f_z = v_z
	f_h = v_h

	return [f_v_x, f_v_z, f_v_h, f_x, f_z, f_h]

# вызываем функция решения системы дифференциальных уравнений из scipy
args_t_arrays = odeint(func, [v_0, 0, 0, 0, 0, H], t)

# получаем выходные функции - интерполируем массивы результатов
x_t = interp1d(t, args_t_arrays[:, 3], "nearest", fill_value = "extrapolate")
z_t = interp1d(t, args_t_arrays[:, 4], "nearest", fill_value = "extrapolate")
h_t = interp1d(t, args_t_arrays[:, 5], "nearest", fill_value = "extrapolate")

# находим время призмеления для изъятия конечных координат - обратная функция t(h), при h = 0 - точка приземления
t_landind = inversefunc(h_t, y_values = 0)

# находим координаты приземления по x и z
x_result = x_target + x_t(t_landind)
z_result = z_target + z_t(t_landind)


# ВИЗУАЛИЗАЦИЯ И ВСЕ ДЕЛА - ОНА НУЖНА НОРМАЛЬНАЯ 

# для красивой визуализации - ограничиваем ось врмемени временем приземления
t_vision = linspace(0, ceil(t_landind), 10000)
x_t_vision = array(x_t(t_vision))
z_t_vision = array(z_t(t_vision))
h_t_vision = array(h_t(t_vision))

x_t_vision += x_target  # Поднимаем графики, в соотвествии с конечными координатами
z_t_vision += z_target  # - / / -

# ОТСЮДА - ИСКЛЮЧИТЕЛЬНО РАБОТА С ОКНАМИ

# 2d - графики - координат от времени
figure_2d_coordinates, axe = subplots(num  = 'Координаты от времени')
title("Графики зависимостей координат от времени")
xlabel("Время, в секундах")
ylabel("Координаты, в метрах")
axe.plot(t_vision, x_t_vision, color = "red")
axe.plot(t_vision, h_t_vision, color = "blue")
axe.plot(t_vision, z_t_vision, color = "green")
legend(("x(t)", "y(t)", "z(t)"))

# 3d - график - траектория от времени
figure_3d_trajectory = figure(num = 'Траектория движения')
title("Траектория полета тела")
ax = axes(projection='3d')
plot(xs = x_t_vision, zs = z_t_vision, ys = h_t_vision, zdir = 'y')
ax.set_xlabel('x coordinate, meters')
ax.set_ylabel('z coordinate, meters')
ax.set_zlabel('height, [y coordinate], meters');


show()
