import csv
import random
import copy

from xlsxwriter import *


days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
stayback_zone = ["Chinese Bowls", "Malay Bowls", "Vending Machine",
                 "Bio Lab Corridor", "Ground Floor", "CSK 2", "Toilet"]

workbook_ = Workbook('Dutylist.xlsx')

header_format = workbook_.add_format({
    "font_name": "PublicoText-Roman",
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'font_size': 14
})

sub_format = workbook_.add_format({
    "font_name": "PublicoText-Roman",
    'border': 1,
    'align': 'left',
    'valign': 'vcenter',
    'font_size': 11
})


def main():

    # load idlist of prefects
    with open('idlist.csv', newline='') as csvfile:

        next(csvfile)
        idlist = people()

        reader = csv.reader(csvfile)
        for i in reader:
            prefect = Prefect()
            prefect.name, prefect.form = i[1], i[2]

            idlist.prefects[i[0]] = prefect
            idlist.committees(i, prefect)

        # for i in idlist.prefects:
        #     print(i, idlist.prefects[i].name, idlist.prefects[i].form)

        # print("\n")
        # for i in idlist.committee:
        #     print(idlist.committee[i].name, idlist.committee[i].form)

        # print("\n")
        # for i in idlist.normal:
        #     print(idlist.normal[i].name, idlist.normal[i].form)

        # print("\n")
        # for i in idlist.probate:
        #     print(idlist.probate[i].name, idlist.probate[i].form)

    # load and assign dutyspots
    with open('dutyspot.csv', newline='') as csvfile:

        next(csvfile)
        dutyspots = {
            "morning": dict(),
            "jr_recess": dict(),
            "sr_recess": dict()
        }

        reader = csv.reader(csvfile)

        # get all the dutyspots
        for i in reader:

            if int(i[1]) == 1:
                dutyspots["morning"][i[0]] = i[2:4]

            if int(i[4]) == 1:
                dutyspots["jr_recess"][i[0]] = i[5:7]

            if int(i[7]) == 1:
                dutyspots["sr_recess"][i[0]] = i[8:10]

        # for i in dutyspots:
        #     print(i)
        #     for j in dutyspots[i]:
        #         print(j, dutyspots[i][j])
        #     print("\n")

        # assign duty
        dutylist = assign_duty(dutyspots, idlist)

    # for i in dutylist:
    #     print(i)
    #     for j in dutylist[i]:
    #         for k in dutylist[i][j]:
    #             print(f"{k} | ", end="")
    #             for l in dutylist[i][j][k]:
    #                 print(f"{l} ", end="")
    #             print("\n")
    #     print("\n")

    morning_write(dutylist, idlist)
    jr_recess_write(dutylist, idlist)
    sr_recess_write(dutylist, idlist)

    workbook_.close()


def jr_recess_write(dutylist, idlist):
    """
    Function to write jr recess dutylist and attendance list
    """

    worksheet3 = workbook_.add_worksheet()

    worksheet3.set_column('A:D', 20)

    worksheet3.merge_range(
        "A1:D1", "Junior Prefectorial Board 2021/2022", header_format)

    worksheet3.merge_range("A2:D2", "Recess duty: ", sub_format)

    # canteen counters
    worksheet3.merge_range("A4:B4", "Canteen Counters - Jr C1", header_format)

    index1 = recess_write(4, 0, 5, "A", dutylist, idlist,
                          worksheet3, "jr_recess", 1, sub_format)

    # canteen tables
    worksheet3.merge_range(
        "C4:D4", "Canteen Tables - Jr Treasurer ", header_format)

    index2 = recess_write(4, 2, 5, "C", dutylist, idlist,
                          worksheet3, "jr_recess", 2, sub_format)

    index = max(int(index1), int(index2)) + 1

    if index > index1:
        incre = index1
        fill_row = ["A", "B"]

    else:
        incre = index2
        fill_row["C", "D"]

    # fill in blanks
    for i in range(1, index - incre, 1):
        worksheet3.merge_range(
            f"{fill_row[0]}{incre -1 +i}:{fill_row[1]}{incre -1 +i}", "-", header_format)

    # quad
    worksheet3.merge_range(
        f"A{index}:B{index}", "Quad - Jr HP", header_format)

    index1 = recess_write(index, 0, index+1, "A", dutylist, idlist,
                          worksheet3, "jr_recess", 3, sub_format)

    # blocks
    worksheet3.merge_range(
        f"C{index}:D{index}", "Blocks - Jr C2", header_format)

    index2 = recess_write(index, 2, index+1, "C", dutylist, idlist,
                          worksheet3, "jr_recess", 4, sub_format)

    # fill blanks
    index = max(int(index1), int(index2)) + 1

    if index > index1:
        incre = index1
        fill_row = ["A", "B"]

    else:
        incre = index2
        fill_row = ["C", "D"]

    # fill in blanks
    for i in range(1, index - incre, 1):
        worksheet3.merge_range(
            f"{fill_row[0]}{incre -1 +i}:{fill_row[1]}{incre -1 +i}", "-", header_format)

    # index for class duty
    worksheet3.write(index, 0, "Class Duty", workbook_.add_format({
        "font_name": "PublicoText-Roman",
        "underline": 1,
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 12
    }))

    # class duty
    # form 1
    worksheet3.merge_range(f"A{index+2}:C{index+2}",
                           "Form 1 Class Duty", header_format)

    row = class_duty_write(index+3, 0, sub_format, dutylist,
                           idlist, worksheet3, "jr_recess", 5)

    # form 2
    worksheet3.merge_range(f"A{row+1}:C{row+1}",
                           "Form 2 Class Duty", header_format)

    row = class_duty_write(row+2, 0, sub_format, dutylist,
                           idlist, worksheet3, "jr_recess", 6)

    # form 3
    worksheet3.merge_range(f"A{row+1}:C{row+1}",
                           "Form 3 Class Duty", header_format)

    row = class_duty_write(row+2, 0, sub_format, dutylist,
                           idlist, worksheet3, "jr_recess", 7)

    """
    Jr recess attendance list
    """

    worksheet4 = workbook_.add_worksheet()

    worksheet4.set_column("A:A", 15)
    worksheet4.set_column("B:B", 17)
    worksheet4.set_column("C:G", 5)

    duty_area = ["Canteen Counters", "Canteen Tables", "Quad", "Blocks",
                 "Form 1 Class Duty", "Form 2 Class Duty", "Form 3 Class Duty"]
    attendance_write(dutylist, worksheet4, idlist, "jr_recess", duty_area)


def sr_recess_write(dutylist, idlist):
    """
    Function to write sr recess dutylist and attendance list
    """

    worksheet5 = workbook_.add_worksheet()

    worksheet5.set_column('A:D', 20)

    worksheet5.merge_range(
        "A1:D1", "Senior Prefectorial Board 2021/2022", header_format)

    worksheet5.merge_range("A2:D2", "Recess duty: ", sub_format)

    # canteen counters
    worksheet5.merge_range("A4:B4", "Canteen Counters - C5", header_format)

    index1 = recess_write(4, 0, 5, "A", dutylist, idlist,
                          worksheet5, "sr_recess", 1, sub_format)

    # canteen tables
    worksheet5.merge_range(
        "C4:D4", "Canteen Tables - C4", header_format)

    index2 = recess_write(4, 2, 5, "C", dutylist, idlist,
                          worksheet5, "sr_recess", 2, sub_format)

    index = max(int(index1), int(index2)) + 1

    if index > index1:
        incre = index1
        fill_row = ["A", "B"]

    else:
        incre = index2
        fill_row = ["C", "D"]

    # fill in blanks
    for i in range(1, index - incre, 1):
        worksheet5.merge_range(
            f"{fill_row[0]}{incre -1 +i}:{fill_row[1]}{incre -1 +i}", "-", header_format)

    # quad
    worksheet5.merge_range(
        f"A{index}:B{index}", "Quad - C1 & C3", header_format)

    index1 = recess_write(index, 0, index+1, "A", dutylist, idlist,
                          worksheet5, "sr_recess", 3, sub_format)

    # blocks
    worksheet5.merge_range(
        f"C{index}:D{index}", "Blocks - C2", header_format)

    index2 = recess_write(index, 2, index+1, "C", dutylist, idlist,
                          worksheet5, "sr_recess", 4, sub_format)

    # fill blanks
    index = max(int(index1), int(index2)) + 1

    if index > index1:
        incre = index1
        fill_row = ["A", "B"]

    else:
        incre = index2
        fill_row["C", "D"]

    # fill in blanks
    for i in range(1, index - incre, 1):
        worksheet5.merge_range(
            f"{fill_row[0]}{incre -1 +i}:{fill_row[1]}{incre -1 +i}", "-", header_format)

    # index for class duty
    worksheet5.write(index + 3, 0, "Class Duty", workbook_.add_format({
        "font_name": "PublicoText-Roman",
        "underline": 1,
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 12
    }))

    # additional note
    worksheet5.merge_range(f"A{index}:D{index}",
                           "Red - Stayback", sub_format)

    worksheet5.merge_range(f"A{index+1}:D{index+1}",
                           "Black - Proceed to duty", sub_format)

    # class duty
    # form 4
    worksheet5.merge_range(f"A{index+5}:C{index+5}",
                           "Form 4 Class Duty", header_format)

    row = class_duty_write(index+6, 0, sub_format, dutylist,
                           idlist, worksheet5, "sr_recess", 5)

    # form 5
    worksheet5.merge_range(f"A{row+1}:C{row+1}",
                           "Form 5 Class Duty", header_format)

    row = class_duty_write(row+2, 0, sub_format, dutylist,
                           idlist, worksheet5, "sr_recess", 6)

    """
    Sr recess attendance list
    """

    worksheet6 = workbook_.add_worksheet()

    worksheet6.set_column("A:A", 15)
    worksheet6.set_column("B:B", 17)
    worksheet6.set_column("C:G", 5)

    duty_area = ["Canteen Counters", "Canteen Tables", "Quad", "Blocks",
                 "Form 4 Class Duty", "Form 5 Class Duty"]
    attendance_write(dutylist, worksheet6, idlist, "sr_recess", duty_area)


def morning_write(dutylist, idlist):
    """
    Function to write morning dutylist and attendance list
    """

    """
    Morning duty list
    """

    worksheet = workbook_.add_worksheet()

    # title
    worksheet.set_column('B:L', 12)
    worksheet.set_row(1, 40)
    worksheet.merge_range('B2:L2', 'Prefectorial Board Duty List', workbook_.add_format({
        "font_name": "PublicoText-Roman",
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 28}))

    # date in use
    worksheet.set_row(2, 30)
    worksheet.merge_range('B3:L3', 'Date in use: ', workbook_.add_format({
        "font_name": "PublicoText-Roman",
        'border': 1,
        'align': 'left',
        'valign': 'vcenter',
        'font_size': 20}))

    # subtitle
    worksheet.merge_range('B5:D5', 'Morning Blocks Duty ', workbook_.add_format({
        "font_name": "PublicoText-Roman",
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 20}))

    # subtitle 2
    worksheet.merge_range('F5:L5', 'Morning Class Duty ', workbook_.add_format({
        "font_name": "PublicoText-Roman",
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 20}))

    worksheet.set_column("C:C", 33)
    worksheet.set_column("D:D", 35)

    row = 5
    cell_index = 6
    cell_copy = cell_index

    # blocks
    row, cell_index, cell_copy = write(row, 2, cell_index, cell_copy, "morning", "C", "B",
                                       1, "Blocks", dutylist, idlist, worksheet)

    # canteen / toilet
    row, cell_index, cell_copy = write(row, 2, cell_index, cell_copy, "morning", "C", "B",
                                       2, "Area", dutylist, idlist, worksheet)

    # gates
    row, cell_index, cell_copy = write(row, 2, cell_index, cell_copy, "morning", "C", "B",
                                       3, "Gate", dutylist, idlist, worksheet)

    # form 1 to form 3
    worksheet.set_column("G:G", 33)
    worksheet.set_column("H:H", 35)
    row, cell_index, cell_copy = write(5, 6, 6, 6, "morning", "G", "F",
                                       4, "Class", dutylist, idlist, worksheet)

    # form 4 to form 5
    worksheet.set_column("K:K", 33)
    worksheet.set_column("L:L", 35)
    row, cell_index, cell_copy = write(5, 10, 6, 6, "morning", "K", "J",
                                       5, "Class", dutylist, idlist, worksheet)

    # attendance

    """
    Morning attendance list
    """

    worksheet2 = workbook_.add_worksheet()

    worksheet2.set_column("A:A", 15)
    worksheet2.set_column("B:B", 17)
    worksheet2.set_column("C:G", 5)

    duty_area = ["Blocks", "Area", "Gate", "Class duty", "Class duty"]

    attendance_write(dutylist, worksheet2, idlist, "morning", duty_area)


def class_duty_write(row, column, cell_format, dutylist, idlist, worksheet, time, area):
    """
    Function to write class duty
    """

    for i in dutylist[time][f"{area}"]:

        col = copy.deepcopy(column)
        # print(dutylist[time][f"{area}"][i])
        worksheet.write(row-1, column, i, cell_format)

        # write prefect on duty
        for j in dutylist[time][f"{area}"][i]:
            name = idlist.prefects[j].name

            if j[0] == "p":
                worksheet.write(row-1, column+1, name, workbook_.add_format({
                    "font_name": "PublicoText-Roman",
                    'border': 1,
                    'align': 'left',
                    'valign': 'vcenter',
                    'font_size': 11,
                    "font_color": "purple"
                }))

            else:
                worksheet.write(row-1, column+1, name, cell_format)

            column += 1

        if len(dutylist[time][f"{area}"][i]) != 2:
            worksheet.write(row-1, column+1, "-", cell_format)

        row += 1
        column = col

    return row


def attendance_write(dutylist, worksheet, idlist, time, duty_area):
    """
    Create attendance list
    """

    cell_format = workbook_.add_format({
        "border": 1,
        'align': 'left',
        'valign': 'vcenter',
        'font_size': 11
    })

    row = 1
    row_index = 1
    for i in dutylist[time]:

        i = int(i)
        # header
        # area
        worksheet.write(row-1, 0, duty_area[i-1], cell_format)

        # prefect name
        worksheet.write(row-1, 1, "Prefect Name", cell_format)
        column = 2
        for j in days:
            worksheet.write(row-1, column, j, cell_format)
            column += 1

        for j in dutylist[time][f"{i}"]:

            # print(j)
            for k in dutylist[time][f"{i}"][j]:

                # prefect names
                name = idlist.prefects[k].name

                # if probate
                if k[0] == "p":
                    worksheet.write(row_index, 1, name, workbook_.add_format({
                        "border": 1,
                        'align': 'left',
                        'valign': 'vcenter',
                        'font_size': 11,
                        "font_color": 'purple'
                    }))

                else:
                    worksheet.write(row_index, 1, name, cell_format)

                for index in range(0, 5, 1):
                    worksheet.write(row_index, 2+index, "", cell_format)

                row_index += 1

            if len(dutylist[time][f"{i}"][j]) > 1:

                worksheet.merge_range(
                    f'A{row+1}:A{row_index}', j, cell_format)

            else:
                worksheet.write(row_index-1, 0, j, cell_format)

            row = row_index

        row_index += 2
        row = row_index


def write(row, column, cell_index, cell_copy, time, col, col2, area, area_name, dutylist, idlist, worksheet):
    """
    Dynamic function that can write dutyspots given area time and which cell to write on
    """

    cell_format = workbook_.add_format({
        "font_name": "PublicoText-Roman",
        "border": 1,
        'align': 'left',
        'valign': 'vcenter',
        'font_size': 16
    })

    for i in dutylist[time][f"{area}"]:

        # print(dutylist[time][f"{area}"][i])

        # write prefect on duty
        for j in dutylist[time][f"{area}"][i]:
            name = idlist.prefects[j].name

            if j[0] == "p":
                worksheet.write(row, column+1, name, workbook_.add_format({
                    "font_name": "PublicoText-Roman",
                    "border": 1,
                    'align': 'left',
                    'valign': 'vcenter',
                    'font_size': 16,
                    "font_color": 'purple'
                }))

            else:
                worksheet.write(row, column+1, name, cell_format)

            row += 1

        # write duty spot
        if len(dutylist[time][f"{area}"][i]) > 1:

            worksheet.merge_range(
                f'{col}{cell_index}:{col}{cell_index + len(dutylist[time][f"{area}"][i])-1}', i, cell_format)

        else:
            worksheet.write(row-1, column, i, cell_format)

        # prepare for the row
        cell_index = cell_index + len(dutylist[time][f"{area}"][i])

    # area
    worksheet.merge_range(
        f"{col2}{cell_copy}:{col2}{cell_index-1}", area_name, cell_format)

    return row+1, cell_index+1, cell_index+1


def recess_write(row, column, cell_index, col, dutylist, idlist, worksheet, time, area, cell_format):
    """
    Function to write recess duty spots
    """

    for i in dutylist[time][f"{area}"]:

        # print(dutylist[time][f"{area}"][i])

        # write prefect on duty
        for j in dutylist[time][f"{area}"][i]:

            name = idlist.prefects[j].name

            if j[0] == "p":
                worksheet.write(row, column+1, name, workbook_.add_format({
                    "font_name": "PublicoText-Roman",
                    "border": 1,
                    'align': 'left',
                    'valign': 'vcenter',
                    'font_size': 11,
                    "font_color": 'purple'
                }))

            else:

                # if senior recess and have to stay back, mark red
                if time == "sr_recess":
                    if i in stayback_zone:

                        worksheet.write(row, column+1, name, workbook_.add_format({
                            "font_name": "PublicoText-Roman",
                            'border': 1,
                            'align': 'left',
                            'valign': 'vcenter',
                            'font_size': 11,
                            "font_color": "red"
                        }))

                    else:
                        worksheet.write(row, column+1, name, cell_format)

                else:
                    worksheet.write(row, column+1, name, cell_format)

            row += 1

        # write duty spot
        if len(dutylist[time][f"{area}"][i]) > 1:

            worksheet.merge_range(
                f'{col}{cell_index}:{col}{cell_index + len(dutylist[time][f"{area}"][i])-1}', i, cell_format)

        else:
            worksheet.write(row-1, column, i, cell_format)

        # prepare for the row
        cell_index = cell_index + len(dutylist[time][f"{area}"][i])

    return cell_index


def assign_duty(dutyspots, idlist):
    """
    Assign duty for each duty spot
    """

    dutylist = {
        "morning": dict(),
        "jr_recess": dict(),
        "sr_recess": dict()
    }

    # morning duty
    prefect = copy.deepcopy(idlist.normal)
    probate = copy.deepcopy(idlist.probate)
    for duty in dutyspots["morning"]:

        end = False

        num = int(dutyspots["morning"][duty][0])

        area = dutyspots["morning"][duty][1]

        if area not in dutylist["morning"].keys():

            dutylist["morning"][area] = dict()
            dutylist["morning"][area][duty] = []

        else:
            dutylist["morning"][area][duty] = []

        # print(dutylist["morning"][area])

        if num == 1:
            ran_prefect = random.choice(list(prefect))
            dutylist["morning"][area][duty].append(ran_prefect)
            del prefect[ran_prefect]

        else:
            probate_num = random.choice([round(num/2), int(num/2)])

            if area == "5":
                probate_num = random.choices(
                    [round(num/2), 0], k=1, weights=[0.4, 0.6])[0]

            prefect_num = int(num) - int(probate_num)

            n = 0
            while n != probate_num:

                if len(probate.keys()) == 0:
                    break

                ran_probate = random.choice((list(probate)))
                dutylist["morning"][area][duty].append(ran_probate)

                # delete probate
                del probate[ran_probate]

                n += 1

            if n != probate_num:
                prefect_num = num - n

            for i in range(0, prefect_num, 1):

                if len(prefect.keys()) == 0:
                    end = True
                    break

                ran_prefect = random.choice(list(prefect))
                dutylist["morning"][area][duty].append(ran_prefect)

                del prefect[ran_prefect]

            if end == True:
                break

        #     print(duty)
        #     print(dutylist["morning"][area][duty])

        # print("\n")

    # recess duty
    prefect = idlist.forms([1, 2, 3]) | idlist.probate
    for duty in dutyspots["jr_recess"]:

        end = False

        num = int(dutyspots["jr_recess"][duty][0])

        area = dutyspots["jr_recess"][duty][1]
        if area not in dutylist["jr_recess"].keys():
            dutylist["jr_recess"][area] = dict()

        dutylist["jr_recess"][area][duty] = []

        for i in range(0, num, 1):

            if len(prefect.keys()) == 0:
                end = True
                break

            ran_prefect = random.choice(list(prefect))

            dutylist["jr_recess"][area][duty].append(ran_prefect)

            del prefect[ran_prefect]

        sorted(dutylist["jr_recess"][area][duty])

        if end == True:
            break

    #     print(duty)
    #     print(dutylist["jr_recess"][area][duty])

    # print("\n")

    # senior recess duty
    class_duty = list()
    prefect = idlist.forms([4, 5])

    for duty in dutyspots["sr_recess"]:

        end = False

        # number of prefect/ probate supposed to duty at this duty
        num = int(dutyspots["sr_recess"][duty][0])

        area = dutyspots["sr_recess"][duty][1]

        if area in ["5", "6"]:
            pass

        else:

            if area not in dutylist["sr_recess"].keys():
                dutylist["sr_recess"][area] = dict()
                dutylist["sr_recess"][area][duty] = []

            else:
                dutylist["sr_recess"][area][duty] = []

            for i in range(0, num, 1):

                if len(prefect.keys()) == 0:
                    end = True
                    break

                ran_prefect = random.choice(list(prefect))

                dutylist["sr_recess"][area][duty].append(ran_prefect)

                copy_ = copy.copy(ran_prefect)

                del prefect[ran_prefect]

                if duty in stayback_zone:
                    pass

                else:
                    class_duty.append(ran_prefect)

            if end == True:
                break

            # print(duty)
            # print(dutylist["sr_recess"][area][duty])

    # class duty
    for duty in dutyspots["sr_recess"]:

        end = False

        # number of prefect/ probate supposed to duty at this duty
        num = int(dutyspots["sr_recess"][duty][0])

        area = dutyspots["sr_recess"][duty][1]

        if area in ["5", "6"]:

            if area not in dutylist["sr_recess"].keys():
                dutylist["sr_recess"][area] = dict()
                dutylist["sr_recess"][area][duty] = []

            else:
                dutylist["sr_recess"][area][duty] = []

            for i in range(0, num, 1):

                if len(class_duty) == 0:
                    end = True
                    break

                ran_prefect = random.choice(class_duty)
                dutylist["sr_recess"][area][duty].append(ran_prefect)
                class_duty.remove(ran_prefect)

            if end == True:
                break

        # print(duty)
        # print(dutylist["sr_recess"][area][duty])

    return dutylist


class people():
    def __init__(self):
        self.prefects = dict()
        self.committee, self.normal, self.probate = dict(), dict(), dict()

    def forms(self, n):
        """
        get index for the forms in n
        """

        prefect = dict()

        for i in self.normal:
            if int(self.normal[i].form) in n:
                prefect[i] = None

        return prefect

    def committees(self, i, prefect):
        """
        get those that are committee and not commmiteee
        """

        if int(i[3]) == 0:
            self.committee[i[0]] = prefect

        else:

            if i[0][0] == "p":
                self.probate[i[0]] = prefect
            else:
                self.normal[i[0]] = prefect


class Prefect():
    """
    details of 1 prefect
    """

    def __init__(self):
        self.name = None
        self.form = None


main()
