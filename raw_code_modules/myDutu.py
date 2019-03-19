# ПИШУ КАК ДАУН В КОММЕНТАХ ЧТО ВЫ МНЕ СДЕЛАЕТЕ ЭТО МОЯ ВЕТКА

# СПИСОК МОДУЛЕЙ



# СПИСОК ПОНАДОБИВШИХСЯ БИБЛИОТЕК, ПРОДУКТОВ И КРАТКАЯ ИНФОРМАЦИЯ
# Pandas - для работы с таблицами
# SciPy - есть модули для аппроксимации функций, решения дифференциальных уравнений(!!!)
#
#
#
#



# ОПИСАНИЕ ВХОДНЫХ ДАННЫХ
# F.csv - таблица зависимости аэродинамической силы от скорости
# Wind.csv - таблица зависимости силы ветр аи высоты слоя
# H, v_0, m - высота сброса, начальная скорость сброса, масса тела
# (x_land,h_land,z_land) - координаты приземеления
# g = 9.81 - константа


# ОПИСАНИЕ ВЫХОДНЫХ ДАННЫХ
#
#
#
#
#

# ОПИСАНИЕ АЛГОРИТМА

# ОПИСАНИЕ ФУНКЦИЙ



'''def func_v_x(v, t):
	global m
	func = -F_aer_v(v)  / m  #+ v_wind_h_x(h)
	return func

def func_v_z(v, t):
	global m
	func = -F_aer_v(v)  / m  #+ v_wind_h_z(v)
	return func

def func_v_h(v, t):
	global m
	func = -F_aer_v(v)  / m - 9.81
	return func


def func_t_vh(t, v):
	global m
	func = pow(-F_aer_v(v)  / m - 9.81, -1)
	return func

def func_c_x(c, t):
	return f_v_x(t)

def func_c_z(c, t):
	return f_v_z(t)

def func_c_h(c, t):
	return f_v_h(t)

t = linspace(0, 10000, 10000)
V = linspace(0, 1000000, 10000000)

v_array_x_raw = odeint(func_v_x, v_0 , t)
v_array_z_raw = odeint(func_v_z, 0 , t)
v_array_h_raw = odeint(func_v_h, 0 , t)
t_array_v_raw = odeint(func_t_vh, 0, V)

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
f_vh_t = interp1d(V, t_array_v_raw[:, 0], "nearest", fill_value = "extrapolate")


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

testing = []
for i in range(1000):

#f = plt.plot(t, v_array_h, color = "green")
f = plt.plot(t, , color = "red")
plt.show()'''




'''h = linspace(0, H, H*100)
v = linspace(0, -H, H*100)
t = linspace(0, -H, H*100)


def args_h(args, h):

	global m
	global H

	v, t, v, h, h = args

	v_h = (-F_aer_v(v) / m + 9.81) / v
	t_h = pow(v, -1)
	v_t = -F_aer_v(v) / m + 9.81
	h_t = v
	h_v = v / (-F_aer_v(v) / m + 9.81)

	return [v_h, t_h, v_t, h_t, h_v]

vt_h_array = odeint(args_h, [0.000000001, 0, 0.000000001, 0, 0], h)
'''
'''win = plt.figure(figsize = (30, 30))
ax1 = win.add_subplot(121)
ax2 = win.add_subplot(221)
ax3 = win.add_subplot(211)
ax4 = win.add_subplot(111)
ax5 = win.add_subplot(222)

ax1.set_title("v(h)")
ax2.set_title("t(h)")
ax3.set_title("v(t)")
ax4.set_title("h(t)")
ax5.set_title("h(v)")'''



#f = plt.plot(h, vt_h_array[:, 4],  color = "blue")
'''ax1.plot(h, vt_h_array[:, 0],  color = "red")
ax2.plot(h, vt_h_array[:, 1],  color = "blue")
ax3.plot(t, vt_h_array[:, 2],  color = "green")
ax4.plot(t, vt_h_array[:, 3],  color = "magenta")
ax5.plot(v, vt_h_array[:, 4],  color = "orange")'''

#plt.show()

# найти зависимость t(h) и v_h(h)- !!!

# поиск v_h(h) - таблица
'''def func_vh_h(v, h):
	global m
	func = (-F_aer_v(v) / m + 9.81) / v
	return func
	
vh_h_array = odeint(func_vh_h, 0.1, h)

# поиск v_h(h) - функция

vh_h = interp1d(h, vh_h_array[:, 0], "nearest", fill_value = "extrapolate")

print(vh_h_array)

print("Скорость старта", vh_h(H))
print("Скорость приземления", vh_h(0))
print(h)

f = plt.plot(h, vh_h_array, color = "green")
plt.show()

# поиск t(v) - таблица
def func_t_v(t, v):
	global m
	func = pow((-F_aer_v(v) / m + 9.81), -1)
	return funс
	
t_v_array = odeint(func_t_v, 0, vh_h_array)'''

# поиск t(h) - функция


'''t_v = interp1d(vh_h_array, t_v_array[:, 0], "nearest", fill_value = "extrapolate")

print('at least, we are HERE 2222222')

t_start = t_v(v_h(H))
t_stop = t_v(v_h(0))

print("Время старта", t_start)
print("Время приземления", t_stop)'''

