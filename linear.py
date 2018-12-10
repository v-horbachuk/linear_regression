import matplotlib.pyplot as plt
import math
import argparse


def hypothesis(theta0, theta1, x):
    return theta0 + (theta1 * x)


def standard_error(x, y, theta0, theta1):
    res = 0
    for i in range(len(x)):
        res += (hypothesis(theta0, theta1, x[i]) - y[i]) ** 2
    return math.sqrt(res / len(x) - 2)


def cost_0(x, y, theta0, theta1, len):
    res = 0.
    for n in range(len):
        res += hypothesis(theta0, theta1, x[n]) - y[n]
    return res


def cost_1(x, y, theta0, theta1, len):
    res = 0.
    for n in range(len):
        res += (hypothesis(theta0, theta1, x[n]) - y[n]) * x[n]
    return res

def normalize_x(x: list):
    x_n = list()
    for z in range(len(x)):
        x_n.append((x[z] - min(x))/ (max(x) - min(x)))
    return x_n


def normalize_one(x, km):
    return (x - min(km))/ (max(km) - min(km))


def read_from_file():
    km = list()
    price = list()

    with open("data.csv", "r") as f:
        next(f)
        for line in f:
            k, p = line.rstrip().split(',')
            p.rstrip()
            km.append(int(k))
            price.append(int(p))
    return km, price

def draw_plot(km, price, theta_0, theta_1):
    plt.scatter(km, price)
    plt.plot([min(km), max(km)], [hypothesis(theta_0, theta_1, normalize_one(min(km), km)), hypothesis(theta_0, theta_1, normalize_one(max(km), km))])
    plt.show()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument()

    km, price = read_from_file()
    km = normalize_x(km)
    alpha = 0.1
    theta_0, theta_1 = 0, 0
    t_tmp_0, t_tmp_1 = 0, 0

    while True:
        t_tmp_0 = t_tmp_0 - (alpha * cost_0(km, price, t_tmp_0, t_tmp_1, len(km))) / len(km)
        t_tmp_1 = t_tmp_1 - (alpha * cost_1(km, price, t_tmp_0, t_tmp_1, len(km))) / len(km)
        if t_tmp_0 == theta_0 and t_tmp_1 == theta_1:
            break
        else:
            theta_0, theta_1 = t_tmp_0, t_tmp_1
    draw_plot(km, price, theta_0, theta_1)
    print(theta_0)
    print(theta_1)
    print(km[0])
    print(hypothesis(theta_0, theta_1, normalize_one(km[0], km)))
    print(standard_error(km, price, theta_0, theta_1))
