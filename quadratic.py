from re import T
from turtle import *

import random
import copy
import time

tur = Turtle()
tur.speed(0)
screen = Screen()
screen.bgcolor("black")
screen.screensize(850, 850)
screen.setup(width=1.0, height=1.0)

tur.penup()

points = [(400, -350), (-400, -350), (0, 342)]

for i in points:
    tur.goto(i)
    tur.dot(5, "white")

initial = random.choice(points)

temp_list = copy.deepcopy(points)

temp_list.remove(initial)

next = random.choice(temp_list)

midpoint = (int(round((next[0] + initial[0]) / 2)),
            int(round((next[1] + initial[1]) / 2)))

time.sleep(5)
n = 0
while n < 10000:
    random_point = random.choice(points)

    temp = (int(round((midpoint[0] + random_point[0]) / 2)),
            int(round((midpoint[1] + random_point[1]) / 2)))

    midpoint = temp

    tur.goto(midpoint)
    tur.dot(5, "white")

done()
