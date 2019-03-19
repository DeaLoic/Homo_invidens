from math import sqrt
import pandas as pd
from scipy.interpolate import interp1d


m = float(input("input m: "))
g = 9.81

x = 0
y = float(input("input h: "))
z = 0

speed_x = float(input("input v0: "))
speed_y = 0
speed_z = 0

x_aim = float(input("x target: "))
z_aim = float(input("z target: "))

t = 0
delta_t = float(input("delta t: "))

wind_csv = pd.read_csv("Wind.csv")
f_csv = pd.read_csv("F.csv")


v_wind_h_x = interp1d(wind_csv["Height (m)"], wind_csv["Wx (m/s)"], "nearest", fill_value="extrapolate")
v_wind_h_z = interp1d(wind_csv["Height (m)"], wind_csv["Wz (m/s)"], "nearest", fill_value="extrapolate")
f_aer_v = interp1d(f_csv["V(m/s)"], f_csv["F(N)"], "nearest", fill_value="extrapolate")


trajectory = pd.DataFrame(columns=["t", "x", "y", "z", "speed_x", "speed_y", "speed_z"])
trajectory.loc[0] = [t, x, y, z, speed_x, speed_y, speed_z]
N = 1

while y > 0:
    speed_air_x = v_wind_h_x(y) - speed_x
    speed_air_y = - speed_y
    speed_air_z = v_wind_h_z(y) - speed_z

    speed_air_full = sqrt(speed_air_x * speed_air_x + speed_air_y * speed_air_y + speed_air_z * speed_air_z)

    f_cur_v = f_aer_v(speed_air_full)

    speed_x_next = speed_x - (f_cur_v * speed_air_x / speed_air_full) * delta_t / m
    speed_y_next = speed_y - g * delta_t + (f_cur_v * speed_air_y / speed_air_full) * delta_t / m
    speed_z_next = speed_z - (f_cur_v * speed_air_z / speed_air_full) * delta_t / m

    x += (speed_x_next + speed_x) / 2 * delta_t
    y += (speed_y_next + speed_y) / 2 * delta_t
    z += (speed_z_next + speed_z) / 2 * delta_t

    speed_x = speed_x_next
    speed_y = speed_y_next
    speed_z = speed_z_next

    t += delta_t

    trajectory.loc[N] = [t, x, y, z, speed_x, speed_y, speed_z]
    N += 1

delta_x = x_aim - trajectory.loc[N - 1][1]
delta_z = z_aim - trajectory.loc[N - 1][3]


trajectory.loc[N-1][2] = 0
trajectory["x"] += delta_x
trajectory["z"] += delta_z

trajectory.to_csv('Trajectory.csv')

print("Angle: 0\nX0: {}\nZ0: {}".format(trajectory.loc[0]["x"], trajectory.loc[0]["z"]))

