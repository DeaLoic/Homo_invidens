from scipy.optimize import newton
def f(x):
    return -x**2 + 4


print(newton(f, 1))
