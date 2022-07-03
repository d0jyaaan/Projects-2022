import numpy as np
from io import StringIO

input_string = '''
25 2 50 1 500 127900
39 3 10 1 1000 222100
13 2 13 1 1000 143750
82 5 20 2 120 268000
130 6 10 2 600 460700
115 6 10 1 550 407000
'''

# this just changes the output settings for easier reading
np.set_printoptions(precision=1)


def fit_model(input_file):
    # Please write your code inside this function

    # read the data in and fit it. the values below are placeholder values

    y = []
    inputs = []
    for i in input_file:
        data = i.split()
        string = []

        for j in data:
            string.append(int(j))

        if len(string) != 0:
            inputs.append(string[0:5])
            y.append(string[5])

    y = np.array(y)
    x = np.array(inputs)  # input data to the linear regression

    # print(x)
    # print(y)
    c = np.linalg.lstsq(a=x, b=y, rcond=None)[0]

    print(c)
    print(x @ c)


# simulate reading a file
input_file = StringIO(input_string)
fit_model(input_file)
