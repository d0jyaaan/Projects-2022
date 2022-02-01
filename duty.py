import csv
import random
import copy
import sys
import datetime
import xlsxwriter

namelist = list()
dutylist = list()
result = list()

def main():
    """
    Takes a command line arguement and executes the code according to the requested query
    There must be 2 csv files called : idlist.csv and dutyspot.csv

    Format for idlist.csv:
        ID    NAME    GRADE   GROUP(OPTIONAL)    COMMITTEE

    Format for dutyspot.csv:
        DUTY    NO. PEOPLE    DUTY TIME(AT LEAST 1)
    
    dutymaker() should be changed according to how many 'time of duty' that exists
    """
    # error check
    if not len(sys.argv) == 2:
        
        # print error
        print("Usage: python duty.py Key")
        print("'Help: python duty.py help")
        sys.exit()

    # execute a function
    else:
        # names of prefects
        with open('idlist.csv', newline='') as csvfile:
            
            spamreader = csv.reader(csvfile, quotechar='|')
            next(csvfile)
            for row in spamreader:
                namelist.append(row)

        # duty spots
        with open('dutyspot.csv', newline='') as csvfile:

            spamreader = csv.reader(csvfile, quotechar='|')
            next(csvfile)
            for row in spamreader:
                dutylist.append(row)

        # dutylist generator
        if sys.argv[1] == "dutylist":
            dutymaker()
            sys.exit()

        # idlist
        elif sys.argv[1] == "idlist":
            idlist()
            sys.exit()

        # help function
        elif sys.argv[1] == "help":
            print("Keys")
            print("idlist")
            print("dutylist")
            sys.exit()
        
        # error
        else:
            print("Invalid Key. Use 'python duty.py help' for help.")
            sys.exit()


def idlist():
    """
    print the id list in the following format:
        ID    NAME
    """

    committee_namelist = list()

    # committee posts
    posts = ["Head Prefect", "Assistant Head Prefect", "Secretary", "Assistant Secretary", "Treasurer", 
    "Counsellor 1", "Counsellor 2", "Counsellor 3","Counsellor 4","Counsellor 5", "Junior Head Prefect", 
    "Junior Secretary", "Junior Treasurer", "Junior Counsellor 1", "Junior Counsellor 2"]

    # print header
    now = datetime.datetime.now()
    print(f"Prefectorial Board of {now.year-1}/{now.year}")
    
    # seperate committee and normal prefects
    for row in namelist:
        
        # if is committee
        if row[4] == "TRUE":
            committee_namelist.append(row)

    # committee board
    print("Committee Board")
    for i in range(0, len(committee_namelist), 1):
    
        print(f"{posts[i]} - {committee_namelist[i][1]}")

    print("\n") 
    print("Prefects ID List")

    # print idlist
    for row in namelist:
        print(f"{row[0]} {row[1]}")


def dutymaker():
    """
    Generates a dutylist for morning, junior recess and senior recess duty

    Prints in the following format:
        Duty spot - Name of prefect ID

    Prints "No Prefects" if there isn't enough prefect
    """
    
    temp_names = list()

    # committee board members
    committee = list()
    for row in namelist:
        if row[4] == "TRUE":
            committee.append(row[0])

        else:
            temp_names.append(row)

    # for each type of duty spot
    # Duty, num of people, """Morning, Recess Junior, Recess Senior""" start from list[2]
    for time in range(2, len(dutylist[0]), 1):
        
        print("\n")
        dutyspot = list()
        names = list()

        for name in temp_names:
            # junior recess
            if time == 3:
                
                if name[2] == "2" or name[2] == "3": 
                    names.append(name)
                    num_people = len(names)-1

            # senior recess
            elif time == 4:
                
                if name[2] == "4" or name[2] == "5": 
                    names.append(name)
                    num_people = len(names)-1

            # morning recess or any recess
            else:
                names.append(name)
                num_people = len(names)-1

        temporary_list = list()

        # make sure no repetitions
        seen = list()
        checked = list()        
        
        for duty in dutylist:

            if duty[time] == "TRUE":

                dutyspot.append(duty)

        # run through all duty spots
        for i in dutyspot:
            
            # random duty spot
            random_dutyspot = random.randint(0, len(dutyspot)-1)
            
            while True:
                                
                # if dutyspot already has person
                if dutyspot[random_dutyspot][0] in checked:

                    # get new random duty spot
                    random_dutyspot = random.randint(0, len(dutyspot)-1)

                else: 
                    break

            # temporary list 
            temporary = list()

            temporary.append(dutyspot[random_dutyspot][0])
            
            # if that spot is must have person
            if dutyspot[random_dutyspot][time] == "TRUE":
                
                # if duty spot doesnt have anyone
                if dutyspot[random_dutyspot][0] not in checked:

                    # for how many people should be in 1 duty spot
                    for people in range(0, int(dutyspot[random_dutyspot][1])):

                        # get random id
                        random_number = random.randint(0, num_people)

                        # if no prefects
                        if len(seen) == len(names):

                            temporary.append([None, None])
                        
                        else:

                            while True:
                                
                                # if is committee or is in seen
                                if names[random_number][0] in committee or names[random_number][0] in seen:
                                    # get random id 
                                    random_number = random.randint(0, num_people)

                                else:
                                    break
                            
                            # append to temporary
                            temporary.extend([names[random_number][0], names[random_number][1]])

                            # append to prevent repetition
                            seen.append(names[random_number][0])
                            checked.append(dutyspot[random_dutyspot][0])

                    # append to another list
                    temporary_list.append(temporary)
                    

                else:
                    break
        
        orderedlist = list()
        for duty in dutyspot:

            for j in temporary_list:

                if duty[0] == j[0]:
                    orderedlist.append(j)

        # append temporary list to main results
        result.append(orderedlist)
    
    if not len(result) == 0:

        # make excel file
        excelmaker(result)
        dutylistprint(result)


def dutylistprint(result):
    """
    Print out the dutylist in the terminal
    A simplified version of excelmaker and can be used for error checking
    """

    # print duty list
    count = 0
    for row in result:

        if count == 0:
            print("Morning Duty")
            
        elif count == 1:
            print("Junior Recess Duty")

        elif count == 2:
            print("Senior Recess Duty")

        print("\n")

        for temp in row:
            print(f"{temp[0]} -  ", end="")

            if len(temp) < 3:
                print("No prefects")

            elif len(temp) >= 2:
                for i in range(1, len(temp), 2):
                    
                    print(f"{temp[i+1]} {temp[i]} ", end="")
            
            print("\n")

        count += 1
            
    print("\n")


def excelmaker(duty):
    """
    Make an excel file of all the duty spots
    Input must be a list

    Change row and col to adjust the placements
    """

    workbook = xlsxwriter.Workbook('dutylist.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(1, 6, "Duty")
    worksheet.write(1, 7, "List")

    count = 0
    for time_of_duty in duty:

        # if morning duty
        if count == 0:
            
            # cell location
            row = 4
            col = 2

            worksheet.write(row-1, col, "Morning Duty")

            # go through all dutyspots
            for duty in time_of_duty:

                # write duty spot to excel file
                worksheet.write(row, col, duty[0])

                # if got prefect there
                if not len(duty) < 3:
                    
                    temp_number = 1
                    temp_id = 1

                    # loop for all people there
                    for i in range(0, round((len(duty)-1)/2) , 1):
                        
                        # write id to excel file
                        worksheet.write(row, col + temp_number, duty[temp_id])
                        temp_id += 2
                        temp_number += 1

                else:
                    
                    worksheet.write(row, col + 1, "None")

                row += 1

        # if junior recess duty
        elif count == 1:
            # cell location
            row = 4
            col = 6

            worksheet.write(row-1, col, "Junior Recess Duty")

            # go through all dutyspots
            for duty in time_of_duty:
                
                # write duty spot to excel file
                worksheet.write(row, col, duty[0])

                # if got prefect there
                if not len(duty) < 3:
                    
                    temp_number = 1
                    temp_id = 1

                    # loop for all people there
                    for i in range(0, round((len(duty)-1)/2) , 1):
                        
                        # write id to excel file
                        worksheet.write(row, col + temp_number, duty[temp_id])
                        temp_id += 2
                        temp_number += 1

                else:
                
                    worksheet.write(row, col + 1, "None")

                row += 1

        # if senior recess duty
        elif count == 2:
            # cell location
            row = 4
            col = 10

            worksheet.write(row-1, col, "Senior Recess Duty")

            # go through all dutyspots
            for duty in time_of_duty:

                # write duty spot to excel file
                worksheet.write(row, col, duty[0])  

                # if got prefect there
                if not len(duty) < 3:
                    
                    temp_number = 1
                    temp_id = 1

                    # loop for all people there
                    for i in range(0, round((len(duty)-1)/2) , 1):
                        
                        # write id to excel file
                        worksheet.write(row, col + temp_number, duty[temp_id])
                        temp_id += 2
                        temp_number += 1

                else:
                
                    worksheet.write(row, col + 1, "None")

                row += 1

        # add to count
        count += 1
    
    # close 
    workbook.close()


if __name__ == "__main__":
        main()