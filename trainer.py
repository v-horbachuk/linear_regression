import sys
import math
import json
import argparse
import matplotlib.pyplot as plt


def args_parser():
    parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-g", '--graph', action="store_true", default=False,
                        help="Adds regression plot to the representation")
    parser.add_argument("-e", "--error", action="store_true", default=False,
                        help="Counts standard error for the regression prediction")
    parser.add_argument("-o", "--output", action="store_true", default=False,
                        help="Adds counted theta0 and theta1 to the output")
    parser.add_argument("-a", "--alpha", type=float, default=0.1,
                        help="Define a learning rate. Default is 0.1")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
    args = parser.parse_args()
    return args


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
    return (x - min(km))/(max(km) - min(km))


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
    plt.plot([min(km), max(km)], [hypothesis(theta_0, theta_1, normalize_one(min(km), km)),
                                  hypothesis(theta_0, theta_1, normalize_one(max(km), km))])
    plt.show()


if __name__ == "__main__":
    args = args_parser()

    km, price = read_from_file()
    km = normalize_x(km)
    alpha = args.alpha
    theta_0, theta_1 = 0, 0
    t_tmp_0, t_tmp_1 = 0, 0

    while True:
        t_tmp_0 = t_tmp_0 - (alpha * cost_0(km, price, t_tmp_0, t_tmp_1, len(km))) / len(km)
        t_tmp_1 = t_tmp_1 - (alpha * cost_1(km, price, t_tmp_0, t_tmp_1, len(km))) / len(km)
        if t_tmp_0 == theta_0 and t_tmp_1 == theta_1:
            break
        else:
            theta_0, theta_1 = t_tmp_0, t_tmp_1

    json_data = json.dumps({"theta0": theta_0, "theta1": theta_1})

    with open("data.json", "w") as file:
        file.write(json_data)

    if args.output:
        print(f"Theta[0] = {theta_0}")
        print(f"Theta[1] = {theta_1}")
    if args.error:
        print(f"Standard error: {standard_error(km, price, theta_0, theta_1)}")
    if not args:
        print(args.help)
    if args.graph:
        draw_plot(km, price, theta_0, theta_1)
