import math
import sys
import matplotlib.pyplot as plt
import numpy as np

from fractions import Fraction

alpha = ["a", "b", "c"]

def main():

    print("ax^2 + bx + c")

    input_list = list()

    for i in range(3):

        while True:

            # get input
            temp = input(f"{alpha[i]} : ")

            try:
                integer = int(temp)
                if isinstance(integer, int):

                    if i == 0:
                        if integer == 0:
                            print("The Coefficient 'a' cannot be 0!")

                        else:
                            input_list.append(integer)
                            break
                        
                    else:
                        input_list.append(integer)
                        break

            except ValueError:
                print("Please input an integer!")
                

    # error checking
    if len(input_list) != 3:
        print("An error occured. Please try again")
        sys.exit()

    print("\n")
    # assign the coefficients
    a = input_list[0]
    b = input_list[1]
    c = input_list[2]

    hr()

    # print the function
    printer(a, b, c)
    
    # find the roots
    formula(a, b, c)

    # vertex form and the min / max point
    vertex(a, b, c)

    # slope of the quadratic
    slope(a,b)

    print("\n")
    hr()
    print("\n")

    # graph the function
    graph(a, b, c)


def graph(a, b, c):
    """
    Graph out the quadratic and its slope
    """
    x = np.linspace(-5, 5, 1000)
    y = a*(x**2) + (b*x) + c

    x2 = np.linspace(-10, 10, 1000)
    y2 = 2*a*x + b

    fig, (ax1, ax2) = plt.subplots(1,2)

    # plot
    ax1.plot(x, y)
    ax2.plot(x2, y2)

    # the function title
    title = None
    
    if b > 0:

        if c > 0:
            title = f"{a}x^2 + {b}x + {c}"

        elif c < 0:
            title = f"{a}x^2 + {b}x - {abs(c)}"

        else:
            title = f"{a}x^2 + {b}x"

    elif b < 0:

        if c > 0:
            title = f"{a}x^2 - {abs(b)}x + {c}"

        elif c < 0:
            title = f"{a}x^2 - {abs(b)}x - {abs(c)}"

        else:
            title = f"{a}x^2 - {abs(b)}x"
    
    elif b == 0:

        if c > 0:
            title = f"{a}x^2 + {c}"

        elif c < 0:
            title = f"{a}x^2 - {abs(c)}"

        else:
            title = f"{a}x^2"

    # name the functions

    ax1.set_title(f"Function: {title}")
    if b > 0:
        ax2.set_title(f"Slope : {Fraction(2*a)}x + {Fraction(b)}")

    elif b < 0:
        ax2.set_title(f"Slope : {Fraction(2*a)}x - {abs(Fraction(b))}")
    
    else:
        ax2.set_title(f"Slope : {Fraction(2*a)}x")

    # show the graph
    plt.show()


def slope(a, b):
    """
    Get the slope of the function using differentiation
    """
    print("\n")

    if b > 0:
        print(f"Slope : {Fraction(2*a)}x + {Fraction(b)}")

    elif b < 0:
        print(f"Slope : {Fraction(2*a)}x - {abs(Fraction(b))}")

    else:
        print(f"Slope : {Fraction(2*a)}x")


def hr():
    for i in range(50):
        print("-", end="")


def vertex(a, b, c):
    """
    Calculate the vertex form and find the min / max point
    """

    print("\n")

    # calculate the h and k values
    h = b / (2*a)

    if h < 0:
        h = abs(h)

    elif h > 0:
        h = -h

    k = (-b**2 + 4*a*c) / (4*a)

    # print the vertex form
    print(f"Vertex Form : {a}(x ", end="")

    # if h is more than 0
    if h > 0:
        if len(str(Fraction(h))) > 5:
            print(f"- {round(h, 3)}", end="")

        else:
            print(f"- {Fraction(h)}", end="")
    
    # if h is less than 0
    elif h < 0:

        if len(str(Fraction(abs(h)))) > 5:
            print(f"- {abs(round(h, 3))}", end="")
            
        else:
            print(f"- {Fraction(abs(h))}", end="")

    print("x)^2", end="")

    if k > 0:
        if len(str(Fraction(k))) > 5:
            print(f" + {round(k, 3)}")

        else:
            print(f" + {Fraction(k)}")

    elif k < 0:
        if len(str(Fraction(k))) > 5:
            print(f" - {abs(round(k, 3))}")

        else:
            print(f" - {Fraction(abs(k))}")

    else:
        print("")

    # min / max point
    if a > 0:
        print(f"Minimum point : ({round(h, 3)} , {round(k, 3)})")

    elif a < 1: 
        print(f"Maximum point : ({round(h, 3)} , {round(k, 3)})")


def printer(a, b, c):
    """
    Print the function
    """
    print("\n")

    print(f"Function: {Fraction(a)}x^2", end="")
    if b > 0:
        print(f" + {Fraction(b)}x", end="")
    
    elif b < 0:
        print(f" - {Fraction(abs(b))}x", end="")

    if c > 0:
        print(f" + {Fraction(c)}", end="")

    elif c < 0:
        print(f" - {Fraction(abs(c))}", end="")
    
    print("\n")


def formula(a, b, c):
    """
    Find the discriminant, roots and calculate the intercept form
    """
    x = (b**2) - (4*a*c)
    
    # if has real root
    if x > 0:
        discriminant = math.sqrt(x)
        root1 = (-b + discriminant) / (2*a)
        root2 = (-b - discriminant) / (2*a)
        
        if len(str(Fraction(root1))) > 5 or len(str(Fraction(root2))) > 5:
            print(f"x1 : {round(root1, 3)}")
            print(f"x2 : {round(root2, 3)}")

        else:
            print(f"x1 : {Fraction(root1)}")
            print(f"x2 : {Fraction(root2)}")

    # no real root
    elif x < 0:

        discriminant = math.sqrt(abs(x))
        root1 = (-b + discriminant) / (2*a)
        root2 = (-b - discriminant) / (2*a)

        print("No real root")

        print(f"x : { -b / (2*a) } + { discriminant / (2*a) }i" )
        print(f"x : { -b / (2*a) } - { discriminant / (2*a) }i" )

    # equal roots
    else:
        discriminant = math.sqrt(x)
        root = (-b + discriminant) / (2*a)

        if len(str(Fraction(root))) > 5:
            print(f"x : {root}")
            
        else:
            print(f"x : {Fraction(round(root), 3)}")

    print("\n")
    print(f"Y-intercept : {c}")

if __name__ == "__main__":
    main()
