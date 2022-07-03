import random


def main():

    my_list = ["cats", 'bats']
    ran_num = random.random()

    if ran_num < 0.8:
        favourite = "dogs"

    else:
        random.shuffle(my_list)
        favourite = my_list[0]

    print("I love " + favourite)


main()
