# ИМПОРТЫ МОДУЛЕЙ И БИБЛИОТЕК
import os
import scipy
from scipy import stats
import pandas
# import Statsmodels as stmods
import numpy
# import ols 

# ПРЕДОБРАБОТКА ВХОДНЫХ ДАННЫХ - ФОРМАТИРОВАНИЕИ И КО.
# перевод таблиц.csv в объекты pandas

# АППРОКСИМАЦИЯ ФУНКЦИИ АЭРОДИНАМИЧЕСКОЙ СИЛЫ ОТ СКОРОСТИ ВЕТРА

# theoretical: 
# Аппроксимация = получение функциональной зависимости между данными - заданными таблично или произвольным отображением

# Интерполяция = получение промежуточных значений функции по заданным
# Экстраполяция = продление функциональной зависимости по заданному промежутку

# Интерполяция = аппроксимация, НА ОГРАНИЧЕННОМ УЧАСТКЕ при которой указываются точки, через которые ТОЧНО будет проходить функция
# Аппроксимация ~ интерполяция + экстраполяция - детальки

# Регрессия = математическое выражение/формула, выражающая зависимость зависимой переменной у от независимых переменных х
# В отличие  от аппроксимации - находится регрессионная зависимость, а не функциональная:
# функциональная: один x может отображаться строго в один y
# регерссионная: один x отображается строго в несколько y

# ТАК ПОД АППРОКСИМАЦИЕЙ БУДЕМ ПОНИМАТЬ 
# (((( ОПИСАНИЕ ТАБЛИЧНО ЗАДАННЫХ ФУНКЦИЙ МАТЕМАТИЧЕСКОЙ ЗАВИСИМОСТЬЮ ))))
# Способы интерполяции: (не все, часть)
# 1) Метод ближайшего соседа 
# 2) Линейная интерполяция
# 3) Интерполяционная формула Ньютона
# 4) Метод конечных разностей
# 5) Многочлен Лангранжа
# 6) Схема Эйткена 
# 7) Сплайн - функция

# Способы аппроксимации: 
# 1) Метод наименьших квадратов     -    Навскидку больше не нашла

# Способы регрессионного анализа:  
# 1) Опа опять метод наименьших квадратов как это работает 

f = open('FofV.txt', 'r')
F_sequence = []

for i in f:
	F_sequence.append(float(i.split()[1]))

v_sequence = [i*10 for i in range(0, 28)]
v_sq_sequence = [(i*10)**2 for i in range(0, 28)] 


# метод - 1 - линейная регрессия F от v - scipy
result_method_1 = stats.linregress(v_sequence, F_sequence)

# метод - 2 - линейная регрессия F от v**2 - scipy
result_method_2 = stats.linregress(v_sq_sequence, F_sequence)

# метод - 3 - метод наименьших квадратов - Statsmodels
#result_method_3 = stmods.OLS( HERE CODE NOW )

# метод - 4 - аппроксимация полиномом, точно не знаю, какая - scipy
k = scipy.polyfit(v_sequence, F_sequence, 10)
result_method_4_1_2 = scipy.polyfit(v_sequence, F_sequence, 1)
result_method_4_2 = scipy.polyfit(v_sq_sequence, F_sequence, 1)

# метод - 5 - аппроксимация к известной функции -//- scipy
#result_method_5 = scipy.optimize.curve_fit(y = x**2, v_sequence, F_sequence)

# метод - 7 - интерполяция - scipy 
result_method_7_1 = scipy.interpolate.interp1d(v_sequence, F_sequence, "linear")
result_method_7_2 = scipy.interpolate.interp1d(v_sequence, F_sequence, "quadratic")
result_method_7_3 = scipy.interpolate.interp1d(v_sequence, F_sequence, "cubic")
result_method_7_4 = scipy.interpolate.interp1d(v_sequence, F_sequence, "nearest")

'''result_method_8 = scipy.interpolate.BarycentricInterpolator(xi[, yi, axis])

result_method_9 = scipy.interpolate.barycentric_interpolate(xi, yi, x[, axis])

result_method_10 = scipy.interpolate.BPoly(c, x[, extrapolate, axis])'''

print("result_method_1 = ", result_method_1)
print("result_method_2 = ", result_method_2)
print("k = ", k)
#print("result_method_4_1 = ", result_method_4_1)
print("result_method_4_1_2 = ", result_method_4_1_2)
print("result_method_4_2 = ", result_method_4_2)
#print("result_method_5 = ", result_method_5)
print("result_method_7_1 = ", result_method_7_1)
print("result_method_7_2 = ", result_method_7_2)
print("result_method_7_3 = ", result_method_7_3)

for i in range(10):
	print(result_method_7_1(i*10))
print()
for i in range(10):
	print(result_method_7_2(i*10))
print()
for i in range(10):
	print(result_method_7_3(i*10))
print()
for i in range(10):
	print(result_method_7_4(i*10))
# ПОИСК ОПТИМАЛЬНОГО ПРОМЕЖУТКА РАЗБИЕНИЯ ВРЕМЕНИ - WIP - ХЗХЗХХЗХ

# СОСТАВЛЕНИЕ ТАБЛИЦ

# ПРЕДОБРАБОТКА ВЫХОДНЫХ ДАННЫХ 

# ВЫВОД ВЫХОДНЫХ ДАННЫХ