from math import sqrt, ceil
import pandas as pd
from scipy.interpolate import interp1d

from scipy.integrate import odeint
from scipy.optimize import fsolve
from matplotlib.pylab import linspace
import timeit
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import subplots, plot, show, figure, title, xlabel, ylabel, legend, axes



def test(y, v0, m, delta_t, v_wind_h_x, v_wind_h_z, f_aer_v, x_aim=0, z_aim=0):
    y = y
    g = 9.81
    x = z = 0

    speed_x = v0
    speed_y = 0
    speed_z = 0

    t = 0
    m = m

    trajectory = pd.DataFrame(columns=["t", "x", "y", "z", "speed_x", "speed_y", "speed_z"])
    trajectory.loc[0] = [t, x, y, z, speed_x, speed_y, speed_z]
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

        trajectory.loc[N] = [t, x, y, z, speed_x, speed_y, speed_z]
        N += 1

    delta_x = x_aim - trajectory.loc[N - 1][1]
    delta_z = z_aim - trajectory.loc[N - 1][3]

    trajectory.loc[N - 1][2] = 0
    trajectory["x"] += delta_x
    trajectory["z"] += delta_z

    print("Angle: 0\nX0: {}\nZ0: {}".format(trajectory.loc[0]["x"], trajectory.loc[0]["z"]))
    del trajectory


def test2(H, v_0, m, v_wind_h_x, v_wind_h_z, f_aer_v, samples=100, x_target=0, z_target=0):

    t = linspace(0, H, int(samples * H))

    # Записываем систему дифференциальных уравнений в матричном виде, где func(y, x) = dy / dx
    def func(args, t):
        global m

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

    # вызываем функция решения системы дифференциальных уравнений из scipy
    args_t_arrays = odeint(func, [v_0, 0, 0, 0, 0, H], t)

    # создаем дата-фрейм
    trajectory = pd.DataFrame(args_t_arrays, columns=["speed_x", "speed_z", "speed_y", "x", "z", "y"])
    trajectory["t"] = t
    # print(args_t_arrays)


    
    '''
    # получаем выходные функции - интерполируем массивы результатов
    x_t = interp1d(t, trajectory["x"], "nearest", fill_value="extrapolate")
    z_t = interp1d(t, trajectory["z"], "nearest", fill_value="extrapolate")
    h_t = interp1d(t, trajectory["y"], "nearest", fill_value="extrapolate")

    # находим время призмеления для изъятия конечных координат - обратная функция t(h), при h = 0 - точка приземления
    t_landing = fsolve(h_t, 0.1)[0]
    print(t_landing)

    x_landing = x_t(t_landing)
    z_landing = z_t(t_landing)
    
    print("X {}\nZ {}".format(x_landing, z_landing))
    delta_x = x_target - x_landing
    delta_z = z_target - z_landing
    '''
    print(trajectory)

    # находим конец траектории (последний y < 0 или первый y > 0)
    i = (trajectory["y"].lt(0).idxmax())
    if i == 0:
        i = (trajectory["y"].gt(0).idxmin())

    print(i)
    # отбрасываем ненужную часть
    trajectory = trajectory.loc[0:i, :]

    delta_x = x_target - trajectory.loc[i]["x"]
    delta_z = z_target - trajectory.loc[i]["z"]

    # корректируем траекторию
    trajectory["x"] += delta_x
    trajectory["z"] += delta_z
    print(trajectory)

    
    # 2d - графики - координат от времени
    figure_2d_coordinates, axe = subplots(num  = 'Координаты от времени')
    title("Графики зависимостей координат от времени")
    xlabel("Время, в секундах")
    ylabel("Координаты, в метрах")
    axe.plot(t, trajectory["x"], color = "red")
    axe.plot(t, trajectory["y"], color = "blue")
    axe.plot(t, trajectory["z"], color = "green")
    legend(("x(t)", "y(t)", "z(t)"))

    # 3d - график - траектория от времени
    figure_3d_trajectory = figure(num = 'Траектория движения')
    title("Траектория полета тела")
    ax = axes(projection='3d')
    plot(xs = trajectory["x"], zs = trajectory["z"], ys = trajectory["y"], zdir = 'y')
    ax.set_xlabel('x coordinate, meters')
    ax.set_ylabel('z coordinate, meters')
    ax.set_zlabel('height, [y coordinate], meters');


    show()


wind_csv = pd.read_csv("Wind.csv")
f_csv = pd.read_csv("F.csv")

v_wind_h_x = interp1d(wind_csv["Height (m)"], wind_csv["Wx (m/s)"], "nearest", fill_value="extrapolate")
v_wind_h_z = interp1d(wind_csv["Height (m)"], wind_csv["Wz (m/s)"], "nearest", fill_value="extrapolate")
f_aer_v = interp1d(f_csv["V(m/s)"], f_csv["F(N)"], "nearest", fill_value="extrapolate")


'''
test(y, v0, m, 1, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v)
test(y, v0, m, 0.1, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v)
test(y, v0, m, 0.01, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v)
test(y, v0, m, 0.001, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v)
test(y, v0, m, 0.0001, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v,)
'''

m = float(input("input m: "))
while m != 0:
    y = float(input("input h: "))
    v0 = float(input("input v0: "))
    # delta_t = float(input("input delta_t: "))
    samples = int(input("input samples: "))

    # test(y, v0, m, delta_t=delta_t, v_wind_h_x=v_wind_h_x, v_wind_h_z=v_wind_h_z, f_aer_v=f_aer_v)
    test2(y, v0, m, v_wind_h_x, v_wind_h_z, f_aer_v, samples=samples)

    m = float(input("input m: "))
