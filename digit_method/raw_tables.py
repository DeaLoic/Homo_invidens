import csv
import matplotlib.pyplot as plt
import pandas as pd

g = 9.81
speed_y = 0
y = 1400
t = -0.1
eps = 0.1
fay = 0

v_to_f_data = pd.read_csv('F.csv')
v_to_f_data["k"] = pd.Series(v_to_f_data["F(N)"] / v_to_f_data["V(m/s)"] ** 2, index=v_to_f_data.index)
print(v_to_f_data)


wind_data = pd.read_csv('Wind.csv')
print(wind_data)
'''
fig = plt.figure()
fig.add_subplot(221)

plt.plot(x, y, label='Power')
plt.xlabel('speed')
plt.ylabel('power')
plt.legend()
plt.show()

g = 9.81
speed_y = 0
y = 1400
t = -0.1
eps = 0.1
fay = 0

while y > 0:
    t += eps
    speed_y = speed_y * eps + (g - fay/m) * pow(eps, 2) / 2
    fay = speeds[speed_y]
    y -= speed_y


'''