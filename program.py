import copy
import math
import os
import random
import pandas as pd

fileDir = './test_dataset/'   # Dataset Folder
courses = {}                  # All Courses
rooms = {}                    # All Rooms
studentcourse = {}            # Students Assigned to courses
indstudentcourses = {}        # Courses assigned to students
teachers = []                 # All Teachers
studentnames = []             # All Students
days = 14                     # Examination Period
coursesstudents = {}          # Courses and students

# Coloring Functions

def prRed(skk): print("\033[91m {}\033[00m" .format(skk),   end="")
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk),   end="")
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk),   end="")
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk),   end="")
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk),   end="")
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk),   end="")
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk),   end="")
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk),   end="")

listOfHardConstraints = [
'1. An exam will be scheduled for each course.',
'2. A student is enrolled in at least 3 courses. A student cannot give more than 1 exam \
at a time.',
'3. Exam will not be held on weekends.',
'4. Each exam must be held between 9 am and 5 pm',
'5. Each exam must be invigilated by a teacher. A teacher cannot invigilate two \
exams at the same time.',
'6. A teacher cannot invigilate two exams in a row.'
]

listOfSoftConstraints = [
'1. All students and teachers shall be given a break on Friday from 1-2.',
'2. A student shall not give more than 1 exam consecutively.',
'3. If a student is enrolled in a MG course and a CS course, it is preferred that \
their MG course exam be held before their CS course exam.',
'4. Two hours of break in the week such that at least half the faculty is free in \
one slot and the rest of the faculty is free in the other slot so the faculty \
meetings shall be held in parts as they are now.'
]

# Class defined containing all information about individual exams
class Exam:
    course = ''
    room = []
    teacher = []
    time = ''
    date = 0


def clear():          # function to clear screen
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def importdata():      # Function to import data from files
    global teachers
    read_teachers = pd.read_csv(fileDir + 'teachers.csv')
    teachers = list(read_teachers.iloc[:, 0])
    global studentnames
    read_students = pd.read_csv(fileDir + 'studentNames.csv')
    studentnames = list(read_students.iloc[:, 0])
    read_courses = pd.read_csv(fileDir + 'courses.csv')
    course_codes = list(read_courses.iloc[:, 0])
    course_names = list(read_courses.iloc[:, 1])
    for i in range(len(course_codes)):
        courses[course_codes[i]] = course_names[i]
    read_rooms = pd.read_csv(fileDir + 'rooms.csv')
    room_capacity = list(read_rooms.iloc[:, 1])
    for i in range(len(room_capacity)):
        rooms[i] = room_capacity[i]
    read_studentcourses = pd.read_csv(fileDir + 'studentCourses.csv')
    studentname = list(read_studentcourses.iloc[:, 1])
    course_code = list(read_studentcourses.iloc[:, 2])
    for i in range(len(studentname)):
        studentcourse[i] = (studentname[i], course_code[i])


def createtable(sol): # function converts the given schedule dict into a 2d list
    table = []
    for i in sol.keys():
        if len(sol[i].room) > 1:
            for j in range(len(sol[i].room)):
                ex = [i, sol[i].room[j], sol[i].teacher[j], sol[i].date, sol[i].time]
                table.append(ex)
        else:
            ex = [i, sol[i].room[0], sol[i].teacher[0], sol[i].date, sol[i].time]
            table.append(ex)
    return table


def assignteacherrooms(exam, roomsno):   #function assigns rooms to teachers -> Hard Constraint #6
    for i in range(roomsno):
        random_room_no = random.randint(1, len(rooms.items()))
        flag = True
        while flag:
            for room in exam.room:
                if room == random_room_no:
                    random_room_no = random.randint(1, len(rooms.items()))
                    break
            flag = False
        exam.room.append(random_room_no)
    for i in range(roomsno):
        random_teacher = random.randint(0, len(teachers) - 1)
        flag = True
        while flag:
            for teacher in exam.teacher:
                if teacher == teachers[random_teacher]:
                    random_teacher = random.randint(0, len(teachers) - 1)
                    break
            flag = False
        exam.teacher.append(teachers[random_teacher])


def assigncourses():      # assign courses to students -> Hard Constraint #1
    for student in studentnames:
        indstudentcourses[student] = []
    for item in range(len(studentcourse.items())):
        indstudentcourses[studentcourse[item][0]].append(studentcourse[item][1])
    for student in studentnames:
        if len(indstudentcourses[student]) < 3: # Hard Constraint #2 
            indstudentcourses.pop(student)


def assignstudentstocourse():  # create lists of students enrolled in each course
    global coursesstudents
    for course in courses.keys():
        coursesstudents[course] = []
    for item in range(len(studentcourse.items())):
        coursesstudents[studentcourse[item][1]].append(studentcourse[item][0])


def random_solution():
    sol = {}
    for i in courses.keys():
        exam = Exam()
        exam.room = []
        exam.teacher = []
        roomsno = int(len(coursesstudents[i]) / 28) + 1
        assignteacherrooms(exam, roomsno)
        randtime = random.randint(0, 1)
        if randtime == 0:
            exam.time = 9
        else:
            exam.time = 2
        exam.date = random.randint(1, days)
        sol[i] = exam
    return sol

''' Hard Constraints '''
'''
1. An exam will be scheduled for each course. 
2. A student is enrolled in at least 3 courses. A student cannot give more than 1 exam 
at a time. 
3. Exam will not be held on weekends. 
4. Each exam must be held between 9 am and 5 pm
5. Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same time. 
6. A teacher cannot invigilate two exams in a row.


Constraint 3, 4 are already fulfilled because of the structure of the program
'''

def studentconstraint(sol):   # Checks the number of student clashes in a particular solution -> Hard Constraint #2
    date_list = []
    cost = 0
    for student in indstudentcourses.keys():
        for course in indstudentcourses[student]:
            date_list.append(sol[course].date)
        a = set(date_list)
        if len(a) != len(date_list):
            cost = cost + 1
        date_list = []
    return cost


def teachersconstraint(sol):    # Checks the number of teacher clashes in a particular solution -> Hard Constraint #5
    exams = {}
    cost = 0
    for i in range(1, days + 1):
        exams[i] = []
    for i in sol.keys():
        for j in sol[i].teacher:
            exams[sol[i].date].append(j)
    for i in exams.keys():
        a = set(exams[i])
        if len(a) != len(exams[i]):
            cost = cost + 1
    return cost


def costfunction(sol):   # calculates fitness value of a solution
    cost = 0
    sf2, sf3 = returnSoftConstraintTwoAndThree(sol)
    cost = studentconstraint(sol) * 1 + teachersconstraint(sol) * 1 + sf2 * 0.05 + sf3 * 0.05
    return cost


def getclashes(sol):     # find where clashes occur
    date_list = []
    for student in indstudentcourses.keys():
        for course in indstudentcourses[student]:
            date_list.append(sol[course].date)
        a = set(date_list)
        if len(a) != len(date_list):
            return student
        date_list = []
    return False


def neighboringsolution(solution):  # create neighboring solution
    student = getclashes(solution)
    if not student:
        print("Test")
        date1 = 0
        date2 = 0
        while date1 == date2:
            index1 = random.randint(0, len(solution.items()) - 1)
            index2 = random.randint(0, len(solution.items()) - 1)
            if index1 == index2:
                continue
            date1 = list(solution.values())[index1].date
            date2 = list(solution.values())[index2].date
            time1 = list(solution.values())[index1].time
            time2 = list(solution.values())[index2].time
            if date1 == date2:
                continue
            course1 = list(solution.keys())[index1]
            course2 = list(solution.keys())[index2]
            solution[course1].date = date2
            solution[course2].date = date1
            solution[course1].time = time2
            solution[course2].time = time1
        return solution
    while True:
        random_numbers = random.sample(range(1, days), len(indstudentcourses[student]))
        a = set(random_numbers)
        if len(a) != len(random_numbers):
            continue
        i = 0
        for course in indstudentcourses[student]:
            solution[course].date = random_numbers[i]
            i = i + 1
        break
    return solution


def setupdata():     # set up all prerequisites of the program
    importdata()
    assignstudentstocourse()
    assigncourses()


def sortsol(solution):   # sort solution by date and time
    sol2 = copy.deepcopy(solution)
    sol = list(sol2.values())
    sol3 = list(sol2.keys())
    for i in range(len(sol)):

        # loop to compare array elements
        for j in range(0, len(sol) - i - 1):

            # compare two adjacent elements
            # change > to < to sort in descending order
            if sol[j].date > sol[j + 1].date:
                # swapping elements if elements
                # are not in the intended order
                temp = sol[j]
                temp2 = sol3[j]
                sol[j] = sol[j + 1]
                sol3[j] = sol3[j + 1]
                sol[j + 1] = temp
                sol3[j + 1] = temp2
            if sol[j].time < sol[j + 1].time and sol[j].date == sol[j + 1].date:
                temp = sol[j]
                temp2 = sol3[j]
                sol[j] = sol[j + 1]
                sol3[j] = sol3[j + 1]
                sol[j + 1] = temp
                sol3[j + 1] = temp2
    j = 0
    xdict = {}
    for i in sol3:
        xdict[i] = []
    for i in xdict.keys():
        xdict[i] = sol[j]
        j += 1
    return xdict
''' Soft Constraints '''
'''
Already Fulfilled soft constraint
Soft Constraint #1: All students and teachers shall be given a break on Friday from 1-2.
Soft Constraint #4: Two hours of break in the week such that at least half the faculty is free in 
one slot and the rest of the faculty is free in the other slot so the faculty 
meetings shall be held in parts as they are now.
'''

''' 
1 Function that returns Soft constraint #2 and Soft Constraint #4
Soft Constraint #2: A student shall not give more than 1 exam consecutively.

Soft Constraint #3: If a student is enrolled in a MG course and a CS course, it is preferred that their MG course
 exam be held before their CS course exam
'''

def returnSoftConstraintTwoAndThree(sol):
    studentEnrolledCourses = copy.deepcopy(indstudentcourses)
    examSchedule = copy.deepcopy(sortsol(sol))
    costOfCSCourseOverMGCourse = 0
    costOfConsecutiveExams = 0
    for student, coursesList in studentEnrolledCourses.items():
        examOccured = False
        checkCSCourseInFirstSlot = False
        for course in coursesList:
            for exam in examSchedule.keys():
                # print(schedule)
                if examSchedule[exam].time == 9:  # First check exams of the student in first slot
                    if course == exam:
                        examOccured = True
                        if "CS" in course:
                            checkCSCourseInFirstSlot = True
                else:
                    if course == exam:
                        # print(examOccured)
                        if examOccured:  # Then check exams of the student in 2nd slot
                            costOfConsecutiveExams += 1
                        if "MG" in course and checkCSCourseInFirstSlot:
                            costOfCSCourseOverMGCourse += 1
                        checkCSCourseInFirstSlot = False
                        examOccured = False
    return costOfConsecutiveExams, costOfCSCourseOverMGCourse

def printFulfilledHardConstraints():
    prGreen("Fulfilled Hard Constraints: \n")
    for constraint in listOfHardConstraints:
            prLightGray(constraint + '\n')

def printFulfilledSoftConstraints():
    prCyan("\nFulfilled Soft Constraints: \n")
    for constraint in listOfSoftConstraints:
            prLightGray(constraint + '\n')
    print('\n')

def simulatedanealing():
    temp = 10000
    coolingrate = 1
    currentsol = random_solution()
    bestsol = random_solution()
    currentcost = costfunction(currentsol)
    bestcost = currentcost
    prRed("Initial Cost: " + str(bestcost) + "\n")
    while temp > 1:
        load = "*" * (100 - int(temp / 10)) + "_" * int(temp / 10)
        prGreen("[" + load + "]\n")
        newsol = copy.deepcopy(neighboringsolution(currentsol))
        newcost = costfunction(newsol)
        prYellow("Current Cost: " + str(newcost) + '\n')
        if newcost < currentcost:
            currentsol = newsol
            currentcost = newcost
            bestsol = copy.deepcopy(newsol)
            bestcost = newcost
            if newcost <= 10:
                printFulfilledHardConstraints()
                printFulfilledSoftConstraints()
                break
        else:
            costdiff = newcost - bestcost
            if random.uniform(0, 1) < math.exp(-costdiff / temp):
                currentsol = newsol
                currentcost = newcost
        temp = temp - coolingrate
        clear()
    return createtable(bestsol)


def setday(datalist):
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dt = copy.deepcopy(datalist)
    dy = []
    for i in range(len(dt)):
        dy.append('')
    j = dt[0] - 1
    for i in range(len(dt)):
        if (j > 4):
            j = dt[0] - 1
        dy[i] = day[j]
        if i != len(dt) - 1 and dt[i + 1] > dt[i]:
            j = j + 1
    return dy


def settime(timelist):
    tl = copy.deepcopy(timelist)
    tx = []
    dx = []
    for i in tl:
        if i == 9:
            tx.append("9:00 AM - 12:00 AM")
        elif i == 2:
            tx.append("2:00 PM - 5:00 PM")
    return tx


def setdate(daylist, datelist):
    dx = []
    dl = copy.deepcopy(datelist)
    count = 0
    for i in range(len(dl)-1):
        dx.append(dl[i] + count)
        if daylist[i] == 'Friday' and daylist[i+1] != 'Friday':
            count += 2
        if i == len(dl)-2:
            dx.append(dl[i] + count)
    return dx


def createdataframe(bestsol):   # create Dataframe from table
    result = []
    for i in bestsol:
        result.append([])

    for i in range(len(bestsol)):
        for j in range(len(bestsol[0])):
            result[j].append(bestsol[i][j])
    df = pd.DataFrame(bestsol, columns=["Course Code", "Room Number", "Teacher Name", "Date", "Time Slot"])
    sdf = df.sort_values(by=['Date', 'Room Number'], ascending=True)
    daycol = setday(list(sdf['Date']))
    timecol = settime(list(sdf['Time Slot']))
    datecol = setdate(daycol, list(sdf['Date']))
    sdf.drop(["Date", "Time Slot"], axis=1)
    sdf['Time Slot'] = timecol
    sdf['Day'] = daycol
    sdf['Date'] = datecol
    if os.path.exists('Datesheet.csv'):
        os.remove('Datesheet.csv')

    sdf.to_csv('Datesheet.csv')
    return sdf


prPurple("Press 1 for Two week Schedule\n Press 2 for 3 Week Schedule\n")
x = int(input("Enter Option: "))
if x == 1:
    days = 10
else:
    days = 15
setupdata()
print(createdataframe(simulatedanealing()))
x = input("Press any key to exit")