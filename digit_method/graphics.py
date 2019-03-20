import matplotlib.pyplot as plt
import csv

g = 9.81
m = 100

x = []
y = []

with open("F.csv", "r") as p:
    plots = csv.reader(p, delimiter=',')
    i = 1
    for row in plots:
        if i != 1:
            x.append(float(row[0]))
            y.append(float(row[1]))
        i = 0

fig = plt.figure()
fig.add_subplot(221)

plt.plot(x, y, label='Power')
plt.xlabel('speed')
plt.ylabel('power')
plt.legend()

with open("Wind.csv", "r") as p:
    plots = csv.reader(p, delimiter=',')
    x = []
    y = []
    z = []
    i = 1
    for row in plots:
        if i != 1:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
        else: i = 2

fig.add_subplot(222)
plt.plot(x, y, label='on x')
plt.plot(x, z, label='on z')
plt.xlabel('height')
plt.ylabel('speed')
plt.legend()

fig.add_subplot(222)


print()
plt.show()
plt1.show()