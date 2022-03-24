from cs50 import get_int

# user prompt
checker = True
while checker == True:
    height = get_int("Height: ")
    if height > 0 and height < 9:
        checker = False

# print pyramid
for i in range(0, height, 1):
    # print the space before the #
    for j in range(0, height - i - 1, 1):
        print(" ", end='')

    # print #
    for k in range(0, i + 1, 1):
        print("#", end='')

    # print "  "
    print("  ", end='')
    # print right side of pyramid
    for l in range(0, i + 1, 1):
        print("#", end='')

    # print /n
    print()
