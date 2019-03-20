from math import sqrt
import pandas as pd
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3


def digit_method(y, v0, m, delta_t, v_wind_h_x, v_wind_h_z, f_aer_v, x_aim=0.0, z_aim=0.0):

    g = 9.81

    x = 0
    z = 0

    speed_x = v0
    speed_y = 0
    speed_z = 0


    t = 0

    trajectory = pd.DataFrame(columns=["speed_x", "speed_z", "speed_y", "x", "z", "y", "t"])
    trajectory.loc[0] = [speed_x, speed_z, speed_y, x, z, y, t]
    N = 1

    while y > 0:
        speed_air_x = - v_wind_h_x(y) + speed_x
        speed_air_y = speed_y
        speed_air_z = - v_wind_h_z(y) + speed_z

        speed_air_full = sqrt(speed_air_x * speed_air_x + speed_air_y * speed_air_y + speed_air_z * speed_air_z)

        f_cur_v = f_aer_v(speed_air_full)

        speed_x_next = speed_x - f_cur_v * speed_air_x / speed_air_full * delta_t / m
        speed_y_next = speed_y - g * delta_t + f_cur_v * speed_air_y / speed_air_full * delta_t / m
        speed_z_next = speed_z - f_cur_v * speed_air_z / speed_air_full * delta_t / m

        x += (speed_x_next + speed_x) / 2 * delta_t
        y += (speed_y_next + speed_y) / 2 * delta_t
        z += (speed_z_next + speed_z) / 2 * delta_t

        speed_x = speed_x_next
        speed_y = speed_y_next
        speed_z = speed_z_next

        t += delta_t

        trajectory.loc[N] = [speed_x, speed_z, speed_y, x, z, y, t]
        N += 1
    delta_x = x_aim - trajectory.loc[N - 1]["x"]
    delta_z = z_aim - trajectory.loc[N - 1]["z"]

    trajectory.loc[N - 1]["y"] = 0
    trajectory["x"] += delta_x
    trajectory["z"] += delta_z

    return trajectory


if __name__ == "__main__":
    m = float(input("input m: "))
    y = float(input("input h: "))

    v0 = float(input("input v0: "))

    x_aim = float(input("x target: "))
    z_aim = float(input("z target: "))

    delta_t = float(input("delta t: "))

    wind_csv = pd.read_csv("Wind.csv")
    f_csv = pd.read_csv("F.csv")

    v_wind_h_x = interp1d(wind_csv["Height (m)"], wind_csv["Wx (m/s)"], "nearest", fill_value="extrapolate")
    v_wind_h_z = interp1d(wind_csv["Height (m)"], wind_csv["Wz (m/s)"], "nearest", fill_value="extrapolate")
    f_aer_v = interp1d(f_csv["V(m/s)"], f_csv["F(N)"], "nearest", fill_value="extrapolate")

    trajectory = digit_method(y, v0, m, delta_t, v_wind_h_x,
                 v_wind_h_z, f_aer_v, x_aim=x_aim, z_aim=z_aim)

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

    ax.set_title('v0 = {}, delta_t = {}, m = {}'.format(v0, delta_t, m))

    plt.show()
