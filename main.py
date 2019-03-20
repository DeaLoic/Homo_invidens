from integrate_method import integral_method
from digit_method import digit_method
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3

# Ввод данных
v_0 = float(input("input v0: "))
H = float(input("input h: "))
m = float(input("input m: "))

x_aim = float(input("x target: "))
z_aim = float(input("z target: "))

wind_csv = pd.read_csv("Wind.csv")
f_csv = pd.read_csv("F.csv")

# Подготовка данных

# интерполяция функций
v_wind_h_x = interp1d(wind_csv["Height (m)"], wind_csv["Wx (m/s)"], "nearest", fill_value="extrapolate")
v_wind_h_z = interp1d(wind_csv["Height (m)"], wind_csv["Wz (m/s)"], "nearest", fill_value="extrapolate")
f_aer_v = interp1d(f_csv["V(m/s)"], f_csv["F(N)"], "nearest", fill_value="extrapolate")

trajectory = integral_method(H, v_0, m, v_wind_h_x, v_wind_h_z, f_aer_v,
                             x_target=x_aim, z_target=z_aim)

if len(trajectory.index) == 1\
        or abs(trajectory.loc[len(trajectory.index) - 1]["speed_y"]) <= 10e-6:
    print("----------------------------------")
    trajectory = digit_method(H, v_0, m, 0.01, v_wind_h_z, v_wind_h_z, f_aer_v,
                              x_aim=x_aim, z_aim=z_aim)

print(trajectory)

print("Angle: 0\nX0: {}\nZ0: {}".format(trajectory.loc[0]["x"], trajectory.loc[0]["z"]))

fig = plt.figure()
ax = p3.Axes3D(fig)

line = ax.plot((trajectory['x'] - trajectory.loc[0]["x"]).values,
                trajectory['z'].values,
                trajectory['y'].values
               )[0]

step_cell = max(trajectory.loc[0]["y"], trajectory.loc[0]["x"], trajectory.loc[0]["z"])
ax.set_xlim3d([0, step_cell])
ax.set_xlabel('X')

ax.set_ylim3d([0, step_cell])
ax.set_ylabel('Z')

ax.set_zlim3d([0, step_cell])
ax.set_zlabel('Y')

ax.set_title('v0 = {}, h = {}, m = {}'.format(v_0, H, m))

plt.show()
