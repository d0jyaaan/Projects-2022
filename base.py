VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
OPERANDS =["+", "-", "*", "/"]


def main():

    print("\n")
    # header and instructions
    print("===Base Calculator===")
    print("Operations")
    print("1 : Base Convertion")
    print("2 : Basic Arithmetic")
    
    # get type of operation
    while True:
        operation = input("Operation : ")

        try:
            operation = int(operation)

            if isinstance(operation, int):
                if operation > 0 and operation < 3:
                    break

        except ValueError:
            print("Please input a valid operation!")

    # execute
    if int(operation) == 1:
        print("\n")

        number, original, end = inputs()
        # print(number, original, end)
        converted = base_convert(number, original, end)
        print("\n")
        print(f"{number} (Base {original}) to (Base {end}) = {converted}")

    elif int(operation) == 2:
        
        while True:
            num_of_variables = input("Number of variables : ")
            try:
                num_of_variables = int(num_of_variables)
                if num_of_variables > 0:
                    break

            except ValueError:
                print("Please input an integer!")
        
        print("\n")
        print("** NOTE : Answers are rounded to nearest 0 and will always be positive (absolute value) **")
        print("\n")
        original, end, equation = inputs_2(num_of_variables)
        print("\n")

        print("------------------------------------------")
        string = " " 
        result = string.join(equation).replace(" ", "")
        print(f"{result} (Base {original} to Base {end}) ")
        operate(original, end, equation)
        print("------------------------------------------")
        print("\n")


def operate(original, end, equation):
    """
    Convert to base 10 and parse it into equation
    Do basic arithmetic on it
    Convert the answer to desired base and round it to the nearest answer
    """
    lst = list()
    # convert to base 10 and parse into equation
    for number in range(0, len(equation), 2):

        sum = 0
        for i in equation[number]:
            for j in range(0, len(VALUES), 1):
                if i == VALUES[j]:
                    sum += j
                    sum *= original

        base10 = sum / original

        lst.append(base10)
        # dont append the operand for last variable
        if number + 1 != len(equation):
            lst.append(equation[number + 1])
    
    while len(lst) != 1:

        tracker = list()
        # get the most important operands first ( * or / then + or -)
        for i in range(1, len(lst), 2):
            for j in range(0, len(OPERANDS), 1):
                if lst[i] == OPERANDS[j]:
                    tracker.append((i, j+1))

        tracker = sorted(tracker, key=lambda x: x[1], reverse=True)
        # print(tracker)
        op = int(tracker.pop(0)[0])
        
        # parse into v1 operand v2
        calculate = list()
        for i in range(op-1, op+2):
            calculate.append(lst[i])

        # do basic arithmetic
        product = arithmetic(calculate)

        # append it
        temp_list = list()
        for i in range(0, len(lst), 1):

            if i == op-1:
                temp_list.append(product)

            elif i == op or i == op+1:
                pass

            else:
                temp_list.append(lst[i])
        
        lst = temp_list
        
    print(f"Answer : {end_convert(lst[0], end)}")
    

def arithmetic(calculate):
    """
    Given a list of v1 operand v2,
    calculate the answer
    """

    # variables
    v1 = float(calculate[0])
    v2 = float(calculate[2])

    operand = calculate[1]
    temp = list()

    # add / subtract / multiply / divide
    if operand == "+":
        temp.append(v1 + v2)

    elif operand == "-":
        temp.append(v1 - v2)

    elif operand == "*":
        temp.append(v1 * v2)

    elif operand == "/":
        temp.append(v1 / v2)

    return abs(temp.pop(0))


def inputs_2(n):
    """
    Get inputs for arithmetic operation
    """

    print("Operands")
    print("1 : Add")
    print("2 : Subtract")
    print("3 : Multiply")
    print("4 : Divide")

    while True:
        original = input("Base to convert FROM (2->10 or 16) : ")

        try:
            original = int(original)

            if isinstance(original, int):
                if original == 16:
                    break

                elif original > 1 and original < 11:
                    break

        except ValueError:
            print("Please input an integer!")

    while True:
        end = input("Base to conert TO    (2->10 or 16) : ")

        try:
            end = int(end)

            if isinstance(end, int):
                if end == 16:
                    break

                elif end > 1 and end < 11:
                    break

        except ValueError:
            print("Please input an integer!")
    
    lst = list()
    for i in range(0, int(n), 1):

        while True:
            # get number
            number = input(f"Variable {i + 1}                         : ")

            if number != "":
                error = 0
                for j in number:

                    if j not in VALUES[:original]:
                        error += 1

                if error == 0:
                    lst.append(number)
                    break
            
        if i != int(n)-1:
            # get the operand
            while True:
                operand = input("Operand                            : ")

                try:
                    operand = int(operand)
        
                    if operand > 0 and operand < 5:
                        lst.append(OPERANDS[operand-1])
                        break

                    else:
                        print("Invalid operand")

                except ValueError:
                    print("Invalid operand")

    return original, end, lst


def inputs():
    """
    Prompt for 3 inputs:
        1) number to convert
        2) base to convert from
        3) base to convert to
    """
    while True:
        original = input("Base to convert FROM (2->10 or 16) : ")

        try:
            original = int(original)

            if isinstance(original, int):
                if original == 16:
                    break

                elif original > 1 and original < 11:
                    break

        except ValueError:
            print("Please input an integer!")

    while True:
        end = input("Base to conert TO    (2->10 or 16) : ")

        try:
            end = int(end)

            if isinstance(end, int):
                if end == 16:
                    break

                elif end > 1 and end < 11:
                    break

        except ValueError:
            print("Please input an integer!")

    while True:
        number = input("Number to convert                  : ")
        
        if number != "":
            error = 0
            for i in number:

                if i not in VALUES[:original]:
                    error += 1

            if error == 0:
                break

    return number, original, end


def base_convert(number, original, end):
    """
    Convert to base 10
    """
    # convert it to base 10
    sum = 0
    for i in number:
        for j in range(0, len(VALUES), 1):
            if i == VALUES[j]:
                sum += j
                sum *= original

    base10 = sum / original

    return(end_convert(base10, end))   


def end_convert(base10, end):
    """
    Convert base 10 to desired base
    """
    converted = list()
    # convert base 10 to end base
    while True:

        # divide by the end base
        temp = int(base10 / end)

        # get remainder
        remainder = int(base10 - temp * end)
        converted.append(VALUES[remainder])

        base10 = temp

        if base10 == 0:
            break
    
    # print(converted)
    # convert into string then to int
    converted.reverse()

    str_ing = " " 
    result = str_ing.join(converted).replace(" ", "")

    # print(result)
    return result


if __name__ == "__main__":
    main()
