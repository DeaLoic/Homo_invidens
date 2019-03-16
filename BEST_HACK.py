from math import sqrt


def aerodynamic_force_coef():
    pass


def speed_wind_x(y):
    pass


def speed_wind_z():
    pass


m = float(input())
g = 9.81

x = 0
y = float(input())
z = 0

speed_x = float(input())
speed_y = 0
speed_z = 0

t = 0
delta_t = 0.01

force_coef = aerodynamic_force_coef()

trajectory = [0 for i in range(100000)]
trajectory[0] = [t, x, y, z, speed_x, speed_y, speed_z]
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

x_aim = float(input())
z_aim = float(input())
delta_x = x_aim - trajectory[N - 1][1]
delta_z = z_aim - trajectory[N - 1][3]

for i in range(N):
    trajectory[i][1] += delta_x
    trajectory[i][3] += delta_z

    
