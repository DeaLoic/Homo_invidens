from math import sqrt
import pandas as pd


# Интерполирует таблицу зависимости аэродинамической силы от скорости
# в единую функцию вида F = k * V^2 и возвращает k
def aerodynamic_force_coef():
    pass


# Предварительно карта ветров должна быть интерполирована в кусочную
# функцию из линейных функци вида V_<coord> = k * y + b для всех промежутков
# у1..y2. Функции speed_wind_<coord> возвращают скорость ветра на данной высоте
# по соответствующей координате
def speed_wind_x(y):
    pass


def speed_wind_z(y):
    pass


v_to_f_data = pd.read_csv('F.csv')
v_to_f_data["k"] = pd.Series(v_to_f_data["F(N)"] / v_to_f_data["V(m/s)"] ** 2, index=v_to_f_data.index)

wind_data = pd.read_csv('Wind.csv')

m = float(input("Input m: "))
g = 9.81

x = 0
y = float(input("Input height: "))
z = 0

x_aim = float(input("Input x aim: "))
z_aim = float(input("Input y aim: "))

speed_x = float(input("Input start speed: "))
speed_y = 0
speed_z = 0

t = 0
delta_t = 0.01

force_coef = aerodynamic_force_coef()

trajectory = pd.DataFrame(columns=["t", "x", "y", "z", "Wx", "Wy", "Wz"])
trajectory.loc[0] = [t, x, y, z, speed_x, speed_y, speed_z]
# [t, x, y, z, speed_x, speed_y, speed_z]

print(trajectory)
N = 1

while y > 0:
    speed_air_x = speed_wind_x(y) - speed_x
    speed_air_y = - speed_y
    speed_air_z = speed_wind_z(y) - speed_z

    speed_air_full = sqrt(speed_air_x * speed_air_x + speed_air_y * speed_air_y + speed_air_z * speed_air_z)
    
    speed_x_next = speed_x - force_coef * speed_air_full * speed_air_x * delta_t / m
    speed_y_next = speed_y - g * delta_t + force_coef * speed_air_full * speed_air_y * delta_t / m
    speed_z_next = speed_z - force_coef * speed_air_full * speed_air_z * delta_t / m

    x += (speed_x_next + speed_x) / 2 * delta_t
    y += (speed_y_next + speed_y) / 2 * delta_t
    z += (speed_z_next + speed_z) / 2 * delta_t

    speed_x = speed_x_next
    speed_y = speed_y_next
    speed_z = speed_z_next

    t += delta_t
    
    trajectory[N] = [t, x, y, z, speed_x, speed_y, speed_z]
    N += 1

trajectory[N - 1][2] = 0

# Узнаём требуемую точку попадания и соответственно сдвигаем всю траекторию по горизинтали
delta_x = x_aim - trajectory[N - 1][1]
delta_z = z_aim - trajectory[N - 1][3]

for i in range(N):
    trajectory[i][1] += delta_x
    trajectory[i][3] += delta_z

