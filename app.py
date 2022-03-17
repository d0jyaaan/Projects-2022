import random
import sys
import csv
import timeit
import copy
import os

from flask import *

N = 5

UPLOAD_FOLDER = './data'
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/",  methods=["GET", "POST"])
def homepage():
    """
    display info and instructions
    """
    if request.method == "POST":
        
        # error checking
        if "classes" not in request.files or "subject" not in request.files:
            flash('No file part')
            return redirect(request.url)

        # if not allowed_file(request.files['classes'].filename) or not allowed_file(request.files['subject']):
        #     return redirect(request.url)
        
        # request files
        data_1 = request.files['classes'].read()
        data_2 = request.files['subject'].read()
        
        # load data
        class_dict = dict()
        subj_dict = dict()

        for j in data_2.decode('utf-8').splitlines():
            i= j.split(",")

            teachers = list()
            for teacher in i[3:]:
                if teacher != "":
                    teachers.append(teacher)
            
            details = Subject(i[0], int(i[2]), teachers)
            subj_dict[int(i[1])] = details

        
        for j in data_1.decode('utf-8').splitlines():
            i= j.split(",")
            # detail of the class
            details = Class_details(None)

            for subj in i[1:]:
                if subj != "":
                    details.subjects.append(int(subj))

            class_dict[i[0]] = details

        # generate timetable
        timetable, subjects, classes = main_sub(class_dict, subj_dict)

        # get time schedules
        temp_dict = dict()
        for i in timetable.keys():
            temp_dict[i] = 0
            for j in timetable[i].structure:    
                if len(timetable[i].structure[j]) > temp_dict[i]:
                    temp_dict[i] = len(timetable[i].structure[j])     
                
        return render_template("timetable.html", timetable=timetable, subjects=subjects, classes=classes, max_val=temp_dict)


    else:
        return render_template("index.html")


def allowed_file(filename):
    """
    Used to error check for invalid file extensions
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def main():
    """
    If ran from the terminal
    """
    start = timeit.default_timer()

    if len(sys.argv) == 1:
        app.run(debug=True)

    elif len(sys.argv) == 3:
        
        data_1 = sys.argv[1]
        data_2 = sys.argv[2]
        
        classes, subjects = load_data(data_1, data_2)
        timetable = main_sub(classes, subjects)

    else:
        print("Usage: python schedule.py [class] [subjects]")
        sys.exit()

    # runtime
    stop = timeit.default_timer()
    print("\n""Run Time: ", round(stop - start, 5), "\n") 


def main_sub(classes, subjects):
    """
    All the functions to generate a timetable
    """

    # assign an empty timetable to all the classes
    timetable = assignment(classes, subjects)
    assign_teacher(subjects, classes)

    # total time slots
    sum = 0
    for i in classes.values():
        total = i.get_total(subjects)
        sum += total
    # print(f"Sum : {sum}")

    # generate multiple timetables and return the timetable with best fitness
    for i in range(0, N, 1):

        c_timetable = copy.deepcopy(timetable)
        timetable_generator(subjects, classes, c_timetable, sum)

        # rehabilitate 3 times
        for i in range(0, 3, 1):
            rehabilitate(c_timetable, subjects, classes)

        # if assignment complete, break
        if assignment_complete(c_timetable):

            timetable = copy.deepcopy(c_timetable)

            # print out the result
            for i in timetable.keys():
                print("\n")
                print(i)
                for j in timetable[i].structure.values():
                    for i in j.values():
                        print(f" |{subjects[i[0]].name} , {i[1]}| ", end="")
                    print("\n")

            break
    
    return timetable, subjects, classes


def rehabilitate(timetable, subject, classes):
    """
    Rearrange the slots with suitable subjects
    According to the following:
        - whether the subj is in the day
        - whether the teacher is available
    """

    # get available slots
    slots = list()
    for i in timetable.keys():
        for j in timetable[i].get_available():
            if len(j) != 0:
                slots.append((i, j[0], j[1]))

    # get remaining subjects
    subj = list()
    for i in classes:
        for j in classes[i].teachers:
            count = 0
            for k in timetable[i].structure.values():
                for l in k.values():
                    if l == j:
                        count += 1
            if count != subject[j[0]].minimum:
                for f in range(0, subject[j[0]].minimum - count, 1):
                    subj.append((i, j[0], j[1]))
    
    # rearrange the slots with suitable subject
    for slot in slots:
        for subjs in subj:
            if slot[0] == subjs[0]:
                s = (subjs[1], subjs[2])

                # if subj not in that day 
                if s not in timetable[slot[0]].structure[slot[1]].values():
                    
                    checker = False
                    count = 0
                    for name in timetable:
                        if name != slot[0]:
                            # and there is no clash
                            if slot[2] in timetable[name].structure[slot[1]].keys():
                                if timetable[name].structure[slot[1]][slot[2]] != s:
                                    count += 1
                            else:
                                count += 1

                    if count == len(timetable) - 1:

                        timetable[slot[0]].structure[slot[1]][slot[2]] = s

                        # if there is multiple same subjects in the list
                        track = 0
                        for i in subj:
                            if i == subj:
                                track += 1
                        if track != 1:
                            subj.remove(subjs)
                            for i in range(0, track-1, 1):
                                subj.append(subjs)
                            
                        break

                    else:
                        checker = True

                    if checker:
                        # if there is a clash, try and switch places with values in the same day
                        count2 = 0
                        for i in timetable[slot[0]].structure[slot[1]]:
                            seperate_subj = timetable[slot[0]].structure[slot[1]][i]
                            for name in timetable:
                                if name != slot[0]:
                                    if slot[2] in timetable[name].structure[slot[1]].keys():
                                        if timetable[name].structure[slot[1]][slot[2]] != seperate_subj:
                                            count2 += 1
                                        else:
                                            count2 += 1

                            if count2 == len(timetable) - 1:
                                timetable[slot[0]].structure[slot[1]][i] = s
                                timetable[slot[0]].structure[slot[1]][slot[2]] = seperate_subj
                                # if there is multiple same subjects in the list

                                track = 0
                                for l in subj:
                                    if l == subj:
                                        track += 1
                                if track != 1:
                                    subj.remove(subjs)
                                    for p in range(0, track-1, 1):
                                        subj.append(subjs)

                                break
                
                # if the subj is in that day, look at slot in other days
                else:
                    
                    breaker = False
                    for name in timetable:
                        if name != slot[0]:
                            # go through subject in different days
                            for i in timetable[name].structure:
                                for j in timetable[name].structure[i]:

                                    count3 = 0
                                    seperate_subj = timetable[slot[0]].structure[i][j]
                                    for name2 in timetable:
                                        if name2 != slot[0]:
                                            if j in timetable[name2].structure[i].keys():
                                                if timetable[name2].structure[i][j] != seperate_subj:
                                                    count3 += 1
                                            else:
                                                count3 += 1

                                    if count3 == len(timetable) - 1:
                                        timetable[slot[0]].structure[i][j] = s
                                        timetable[slot[0]].structure[slot[1]][slot[2]] = seperate_subj

                                        track = 0
                                        for i in subj:
                                            if i == subj:
                                                track += 1
                                        if track != 1:
                                            subj.remove(subjs)
                                            for i in range(0, track-1, 1):
                                                subj.append(subjs)

                                        breaker = True
                                        break

                                if breaker:
                                    break
                        if breaker:
                            break


def timetable_generator(subject, classes, timetable, n):
    """
    Generate
    """
    period, domain = periods(classes, timetable)

    # get all the class names
    my_list = list()
    for key in timetable:
        my_list.append(key)
        
    # generate random partial timetable
    count = 0
    while True:
        if count > n:
            break
        # get random class name
        class_name = random.choice(my_list)
        # get random available of the class
        if timetable[class_name].get_available():
            available_slot = random.choice(timetable[class_name].get_available())
            # print(class_name, available_slot)

            if len(domain[class_name][available_slot[0]][available_slot[1]]) != 0:
                # get random subject
                rand_subject = random.choice(domain[class_name][available_slot[0]][available_slot[1]])
                constraints(available_slot, domain, class_name, timetable, classes, subject, rand_subject)
        
        count += 1


def constraints(slot, domain, class_name, timetable, classes, subject, rand_subject):
    """
    check whether the assignment satisfies the constraints 
    and remove any suitable values from the domain
    """

    day = slot[0]
    period = slot[1]

    timetable[class_name].structure[day][period] = rand_subject

    # remove subj from the domain of periods of the same day
    for i in domain[class_name][day].values():
        if rand_subject in i:
            i.remove(rand_subject)

    count = 0
    # get how many times the subject appears
    for i in timetable[class_name].structure.values():
        for j in i.values():
            if j == rand_subject:
                count += 1
    # print(count)
    
    # max
    # print(subject[rand_subject[0]].minimum)
    if count == subject[rand_subject[0]].minimum:
        for i in domain[class_name].values():
            for j in i.values():
                if rand_subject in j:
                    j.remove(rand_subject)

    # teachers
    for name in domain:
        if name != class_name:
            if rand_subject in classes[name].teachers:
                if period in domain[name][day].keys():
                    if rand_subject in domain[name][day][period]:
                        domain[name][day][period].remove(rand_subject)


def periods(classes, timetable):
    """
    Return the number of periods of each subject for every class and the domain of each class
    """

    my_dict = dict()
    domain = dict()

    for name in classes.keys():
        my_dict[name] = dict()
        domain[name] = list()

        # randomize the domain
        random.shuffle(domain[name])

    # assign a domain that contains all the subj to all the periods 
    for name in timetable:
        domain[name] = dict()
        for day in timetable[name].structure:
            domain[name][day] = dict()
            for period in timetable[name].structure[day]:
                lst = list()
                for subj in classes[name].teachers:
                    lst.append(subj)
                        
                domain[name][day][period] = lst
            
    return my_dict, domain


def assignment_complete(timetable):
    """
    Check whether every class has a period
    """
    for structure in timetable.values():
        for day in structure.structure:
            for period in structure.structure[day]:
                # if any period is None, return false
                if structure.structure[day][period] == None:
                    return False
    
    # else return true
    return True
         

def load_data(classes, people):
    """
    Load data into dictionaries that contain details of the data
    """

    # key is the subject code
    subj_dict = dict()
    # key is the class name
    class_dict = dict()

    # subjects
    with open(people, "r") as file:

        lines = csv.reader(file)

        for i in lines:

            teachers = list()
            for teacher in i[3:]:
                if teacher != "":
                    teachers.append(teacher)
            
            details = Subject(i[0], int(i[2]), teachers)
            subj_dict[int(i[1])] = details
    
    # classes
    with open(classes, "r") as f:
        lines_2 = csv.reader(f)
        
        for i in lines_2:
            # detail of the class
            details = Class_details(None)

            for subj in i[1:]:
                if subj != "":
                    details.subjects.append(int(subj))

            class_dict[i[0]] = details

    return (subj_dict, class_dict)


def assignment(classes, subjects):
    """
    Assign empty timetable to all the classes with the following format:
    Class name : {
        Day :{
            Periods
        }
    }
    """
    
    my_dict = dict()

    # assignment
    for name in classes:

        empty = Timetable()

        # get total number of classes
        number = classes[name].get_total(subjects)
        empty.structure = empty.generate(number)
        my_dict[name] = empty
    
    # for i in my_dict.values():
    #     for j in i.structure.keys():
    #         print(j, i.structure[j])

    return my_dict


def assign_teacher(subject, classes):
    """
    Assign teachers to each class with an even distribution
    No return value
    """

    length = len(classes.keys())

    subj_teachers = dict()
    # even distribution
    for subj in subject:

        lst = list()

        for name in subject[subj].teacher:

            rounded = round(length/len(subject[subj].teacher))

            if (rounded * len(subject[subj].teacher)) < length:
                rounded += 1

            for i in range(0, rounded, 1):
                lst.append(name)

        random.shuffle(lst)
        subj_teachers[subj] = lst

    # print(subj_teachers)

    for name in classes.keys():
        lst = list()
        for subj in classes[name].subjects:
            if len(subj_teachers[subj]) != 0:
                lst.append((subj, subj_teachers[subj].pop()))
        classes[name].teachers = lst


class Class_details:
    """
    Class of class details
    """

    def __init__(self, teacher):
        self.subjects = list()
        self.teachers = teacher
        
    def get_total(self, subject):
        """
        Return total of how many periods of classes
        """
        count = 0

        for i in self.subjects:
            count += subject[i].minimum

        return count


class Subject:
    """
    Class of a subject with their code, periods and teachers
    """

    def __init__(self, name, minimum, teacher):
        self.name = name
        self.minimum = minimum
        self.teacher = teacher


class Timetable:
    """
    Structure of the timetable
    Change the day and periods accordingly
    """

    def __init__(self):
        self.structure = None

    def generate(self, number):
        """
        Generate an empty timetable from Monday to Friday
        """
        temp_number = int(number/5)
        my_dict = dict()

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # initial assignment
        for day in days:
            temp_dict = dict()
            for i in range(0, temp_number, 1):
                temp_dict[i] = None
            my_dict[day] = temp_dict

        # if number of periods is not a multiple of 5
        limit = (number - (temp_number * 5))
        if (limit != 0):
            count = 0
            for i in my_dict.values():
                i[len(i)] = None
                count += 1
                if count == limit:
                    break

        return my_dict

    def get_available(self):
        """
        return all the available slots in the timetable
        """
        lst = list()
        for i in self.structure.keys():
            for j in self.structure[i]:
                if self.structure[i][j] is None:
                    lst.append((i, j))

        # print(lst)
        return lst


if __name__ == "__main__":

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    main()

