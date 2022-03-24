import sys
import math
# input prompt
card_num = int(input("Number: "))

# initialise values
credit_card = card_num
total = 0
position = 0
digit_count = 0

# algorithm
while credit_card != 0:
    #  luhn algorithm
    if position % 2 != 0:
        temp = math.trunc((credit_card % 10) * 2)

        if temp > 9:
            total += math.trunc((temp % 10 + (temp / 10) % 10))
        else:
            total += temp

    else:
        total += math.trunc(credit_card % 10)

    #  add to
    digit_count += 1
    position += 1
    credit_card = math.trunc(credit_card / 10)

# round off
total = math.trunc(total)

# check
if total % 10 == 0:
    # first few numbers of card type
    AMEX = math.trunc(card_num / 10000000000000)
    MASTERCARD = math.trunc(card_num / 100000000000000)
    VISA_1 = math.trunc(card_num / 1000000000000)
    VISA_2 = math.trunc(card_num / 1000000000000000)

    # AMEX checker
    if (AMEX == 34 and digit_count == 15) or (AMEX == 37 and digit_count == 15):
        print("AMEX")
        sys.exit(0)

    # mastercard checker
    mastercard = [51, 52, 53, 54, 55]
    if digit_count == 16:
        if MASTERCARD in mastercard:
            print("MASTERCARD")
            sys.exit(0)

    # visa checker 13 digit
    if (VISA_1 == 4 and digit_count == 13):
        print("VISA")
        sys.exit(0)

    # visa checker 16 digit
    if (VISA_2 == 4 and digit_count == 16):
        print("VISA")
        sys.exit(0)

    # if no match print invalid
    else:
        print("INVALID")
        sys.exit(0)

# if not end with 0, print invalid
else:
    print("INVALID")