import scipy


# тут будет норм преобразование из csv в таблицу_pandas или массив_numPy
# но пока тут это
f = open('FofV.txt', 'r')
F_sequence = []

for i in f:
	F_sequence.append(float(i.split()[1]))

v_sequence = [i*10 for i in range(0, 28)]


# аппроксимация к полиному второй степени - поиск коэффициента
k = scipy.polyfit(v_sequence, F_sequence, 2)[0]
