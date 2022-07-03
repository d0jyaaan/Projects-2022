portnames = ["PAN", "AMS", "CAS", "NYC", "HEL"]

# https://sea-distances.org/
# nautical miles converted to km

D = [
    [0, 8943, 8019, 3652, 10545],
    [8943, 0, 2619, 6317, 2078],
    [8019, 2619, 0, 5836, 4939],
    [3652, 6317, 5836, 0, 7825],
    [10545, 2078, 4939, 7825, 0]
]

# https://timeforchange.org/co2-emissions-shipping-goods
# assume 20g per km per metric ton (of pineapples)

co2 = 0.020

# DATA BLOCK ENDS

# these variables are initialised to nonsensical values
# your program should determine the correct values for them
smallest = 1000000
bestroute = [0, 0, 0, 0, 0]


def permutations(route, ports):
    # write the recursive function here
    # remember to calculate the emissions of the route as the recursion ends
    # and keep track of the route with the lowest emissions

    global smallest
    global bestroute

    for i in ports:

        my_list = route + [i]
        new_ports = [x for x in ports if x not in my_list]

        if len(new_ports) != 0:
            permutations(my_list, new_ports)

        else:
            # calculate total distance
            sum = 0

            for x in range(len(my_list)-1):

                a = my_list[x]
                b = my_list[x+1]
                sum += D[a][b]

            # calculate carbon emission
            emission = sum * co2

            if emission < smallest:
                # print(emission)
                smallest = emission
                bestroute = my_list


def main():
    # Do not edit any (global) variables using this function, as it will mess up the testing

    # this will start the recursion
    permutations([0], list(range(1, len(portnames))))

    # print the best route and its emissions
    print(' '.join([portnames[i] for i in bestroute]) + " %.1f kg" % smallest)


main()
