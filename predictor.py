import json
from trainer import read_from_file, normalize_one, hypothesis, normalize_x

try:
    user_input = int(input("Enter car millage, miles: "))
except:
    print("Input millage must be an integer. Start the program once more with a correct input")
    exit(1)

try:
    with open("data.json", "r") as file:
        data = json.load(file)
        theta_0 = data['theta0']
        theta_1 = data['theta1']
except:
    theta_0 = 0
    theta_1 = 0

km, price = read_from_file()
km.append(user_input)
km = normalize_x(km)

print(f"Estimated price: {hypothesis(theta_0, theta_1, normalize_one(km[-1], km))}")
