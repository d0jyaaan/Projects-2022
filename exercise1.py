portnames = ["PAN", "AMS", "CAS", "NYC", "HEL"]


def permutations(route, ports):
    # Write your recursive code here
    for i in ports:

        my_list = route + [i]
        new_ports = [x for x in ports if x not in my_list]

        if len(new_ports) != 0:
            permutations(my_list, new_ports)

        else:
            route = my_list
            # Print the port names in route when the recursion terminates
            print(' '.join([portnames[i] for i in route]))


# This will start the recursion with 0 ("PAN") as the first stop
permutations([0], list(range(1, len(portnames))))
