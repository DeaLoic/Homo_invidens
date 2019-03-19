from math import sqrt
from input_data import m, g, H, V_start, x_aim, z_aim, F_from_V, Wind_x, Wind_z, delta_t


x = 0
y = H
z = 0

speed_x = V_start
speed_y = 0
speed_z = 0

t = 0

trajectory = pd.DataFrame({'Time': [], 'X': [], 'Y': [], 'Z': [],
                           'Speed_x': [], 'Speed_y': [], 'Speed_z': []})
trajectory.loc[0] = t, x, y, z, speed_x, speed_y, speed_z
i = 1

while y > 0:
    speed_air_x = Wind_x(y) - speed_x
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
x_aim = float(input())
z_aim = float(input())
delta_x = x_aim - trajectory[N - 1][1]
delta_z = z_aim - trajectory[N - 1][3]

for i in range(N):
    trajectory[i][1] += delta_x
    trajectory[i][3] += delta_z

    
