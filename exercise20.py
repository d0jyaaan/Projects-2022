import math
import numpy as np

x = np.array([4, 3, 0])
c1 = np.array([-.5, .1, .08])
c2 = np.array([-.2, .2, .31])
c3 = np.array([.5, -.1, 2.53])


def sigmoid(z):
    # add your implementation of the sigmoid function here
    denominator = 1 + math.exp(-z)
    value = 1 / denominator
    return value


# calculate the output of the sigmoid for x with all three coefficients
my_list = []
my_list.append(x @ c1)
my_list.append(x @ c2)
my_list.append(x @ c3)

values = []
for value in my_list:
    sigmoid_value = sigmoid(value)
    print(sigmoid_value)

    values.append(sigmoid_value)

max = np.argmax(np.array(values))
print(max)
