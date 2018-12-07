import numpy as np
import matplotlib as mtp
import math


def equasion(theta0, theta1, x):
    return theta0 + (theta1 * x)


def cost_0(x, y, theta0, theta1, len):
    res = 0.
    for n in range(len-1):
        res += equasion(theta0, theta1, x[n]) - y[n]
    return res / len


def cost_1(x, y, theta0, theta1, len):
    res = 0.
    for n in range(len-1):
        res += (equasion(theta0, theta1, x[n]) - y[n]) * x[n]
    return res / len


def normalize_x(x: list):
    x_n = list()
    print(max(x), min(x))
    for z in range(len(x)):
        x_n.append((x[z] - min(x))/ (max(x) - min(x)))
    return x_n

def normalize_one(x, km):
    return (x - min(km))/ (max(km) - min(km))

def estimate(t0, t1, km, price, l_rate):
    t0_tmp = 0
    t1_tmp = 0
    for i in range(len(km)):
        t0_tmp += equasion(t0, t1, km[i]) - price[i]
        t1_tmp += ((equasion(t0, t1, km[i])) - price[i]) * km[i]
    t0 = t0 - (l_rate * t0_tmp) / len(km)
    t1 = t1 - (l_rate * t1_tmp) / len(km)
    return t0, t1

if __name__ == "__main__":
    km = list()
    price = list()
    with open("data.csv") as f:
        for line in f:
            k, p = line.rstrip().split(',')
            p.rstrip()
            if k == 'km':
                continue
            elif p == 'price':
                continue
            km.append(int(k))
            price.append(int(p))

    alpha = 0.1
    theta_0 = 0
    theta_1 = 0
    km_n = normalize_x(km)
    # price_n = normalize_x(price)
    price_n = price
    print(km_n, price_n)
    t_tmp_0 = 0
    t_tmp_1 = 0
    while True:
        t_tmp_0, t_tmp_1 = estimate(theta_0, theta_1, km_n, price_n, alpha)
        if t_tmp_0 == theta_0 and t_tmp_1 == theta_1:
            break
        else:
            theta_0, theta_1 = t_tmp_0, t_tmp_1
    print(theta_0)
    print(theta_1)
    print(km[0])
    print(equasion(theta_0, theta_1, normalize_one(km[0], km)))
