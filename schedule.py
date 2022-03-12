from itertools import count
import random
import sys
import csv

N = 500

def main():
    if len(sys.argv) != 3:
        print("Usage: python schedule.py class subjects")
        sys.exit()

    data_1 = sys.argv[1]
    data_2 = sys.argv[2]

    # load the data into dicts
    subjects, classes = load_data(data_1, data_2)

    # assign an empty timetable to all the classes
    timetables = assignment(classes, subjects)
    assign_teacher(subjects, classes)

    # generate timetable
    timetable_generator(subjects, classes, timetables, N)

    # for i in timetables.keys():
    #     print(i)
    #     for j in timetables[i].get_available():
    #         print(j)
    #     print("\n")


def timetable_generator(subject, classes, timetable, n):
    """
    Generate
    """
    period, domain = periods(subject, classes, timetable)
    # print(domain)

    # get all the class names
    my_list = list()
    for key in timetable:
        my_list.append(key)

    # assign 
    count = 0
    while True:

        # if assignment is complete, return
        if assignment_complete(timetable):
            return timetable

        # if stuck in a loop, after n iterations, return false
        if count > n:
            return False

        # get random class name
        class_name = random.choice(my_list)
        # get random available of the class
        available_slot = random.choice(timetable[class_name].get_available())
        # print(class_name, available_slot)

        if len(domain[class_name]) != 0:
            # get random subject
            rand_subject = domain[class_name].pop()
            if constraints(available_slot, domain, class_name, timetable, classes, rand_subject):
                break
        
        else:
            pass

        count += 1
        

def constraints(slot, domain, name, timetable, classes, subject):
    """
    check whether the assignment satisfies the constraints 
    and remove any suitable values from the domain
    """

    # IMPO : iterate through the original but use a deepcopy to keep new values
    print("\n\n",slot,"\n\n", domain,"\n\n", name,"\n\n", timetable,"\n\n", classes,"\n\n", subject)
    for name in domain:
        print(name)
        print(domain[name])

    return True


def periods(subject, classes, timetable):
    """
    Return the number of periods of each subject for every class and the domain of each class
    """

    my_dict = dict()
    domain = dict()

    for name in classes.keys():
        my_dict[name] = dict()
        domain[name] = list()

        # for id in classes[name].subjects:
        #     # get the domain
        #     for number in range(0, subject[id].minimum, 1):  
        #         for i in classes[name].teachers:
        #             if i[0] == id:
        #                 domain[name].append(i)

            # my_dict[name][id] = subject[id].minimum
            # print(my_dict[name][id])

        # randomize the domain
        random.shuffle(domain[name])

    for name in timetable:
        for day in timetable[name].structure:
            domain[day] = dict()
            for period in timetable[name].structure[day]:
                lst = list()
                for i in classes.values():
                    for subj in i.teachers:
                        lst.append(subj)
                domain[day][period] = lst
                # domain[day][period] = 
    
    for i in domain.values():
        for j in i.values():
            print(j)
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

        # skip first line
        next(lines)

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
    Assign teachers to each class
    No return value
    """
    for name in classes.keys():
        lst = list()
        # for each subj, assign a teacher to it
        for subj in classes[name].subjects:
            lst.append((subj ,random.choice(subject[subj].teacher)))
        # append
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
        temp_number = int(number/ 5)
        my_dict = dict()

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # initial assignment
        for day in days :
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
                lst.append((i, j))
            
        # print(lst)
        return lst


if __name__ == "__main__":
    main()
