import copy
import math
import os
import random
import pandas as pd
import time


fileDir = './actual_dataset/'
courses = {}
rooms = {}
studentEnrolledCourses = {}
indstudentcourses = {}
teachers = []
studentnames = []
days = 14
coursesstudents = {}

def prRed(skk): print("\033[91m {}\033[00m" .format(skk),   end="")
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk),   end="")
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk),   end="")
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk),   end="")
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk),   end="")
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk),   end="")
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk),   end="")
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk),   end="")

listOfHardConstraints = [
'• An exam will be scheduled for each course.',
'• A student is enrolled in at least 3 courses. A student cannot give more than 1 exam \
at a time.',
'• Exam will not be held on weekends.',
'• Each exam must be held between 9 am and 5 pm',
'• Each exam must be invigilated by a teacher. A teacher cannot invigilate two \
exams at the same time.',
'• A teacher cannot invigilate two exams in a row.'
]

listOfSoftConstraints = [
'• All students and teachers shall be given a break on Friday from 1-2.',
'• A student shall not give more than 1 exam consecutively.',
'• If a student is enrolled in a MG course and a CS course, it is preferred that \
their MG course exam be held before their CS course exam.',
'• Two hours of break in the week such that at least half the faculty is free in \
one slot and the rest of the faculty is free in the other slot so the faculty \
meetings shall be held in parts as they are now.'
]

class Exam:
    course = ''
    room = []
    teacher = []
    time = ''
    date = 0

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')



def importdata():
    global teachers, studentnames
    read_teachers = pd.read_csv(fileDir + 'teachers.csv')
    teachers = list(read_teachers.iloc[:, 0])
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
        studentEnrolledCourses[i] = (studentname[i], course_code[i])


def createtable(sol):
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


def assignteacherrooms(exam, roomsno):
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


def assigncourses():
    for student in studentnames:
        indstudentcourses[student] = []
    for item in range(len(studentEnrolledCourses.items())):
        indstudentcourses[studentEnrolledCourses[item][0]].append(studentEnrolledCourses[item][1])
    for student in studentnames:
        if(len(indstudentcourses[student]) < 3):
            indstudentcourses.remove(student)

def assignstudentstocourse():
    global coursesstudents
    for course in courses.keys():
        coursesstudents[course] = []
    for item in range(len(studentEnrolledCourses.items())):
        coursesstudents[studentEnrolledCourses[item][1]].append(studentEnrolledCourses[item][0])


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




def studentconstraint(sol):
    date_list = []
    for student in indstudentcourses.keys():
        for course in indstudentcourses[student]:
            date_list.append(sol[course].date)
        a = set(date_list)
        if len(a) != len(date_list):
            return False
        date_list = []
    return True


def teachersconstraint(sol):
    exams = {}
    for i in range(1, days + 1):
        exams[i] = []
    for i in sol.keys():
        for j in sol[i].teacher:
            exams[sol[i].date].append(j)
    for i in exams.keys():
        a = set(exams[i])
        if len(a) != len(exams[i]):
            return False
    return True


''' 
1 Function that returns Soft constraint #2 and Soft Constraint #4
Soft Constraint #2: A student shall not give more than 1 exam consecutively.

Soft Constraint#3: If a student is enrolled in a MG course and a CS course, it is preferred that their MG course
 exam be held before their CS course exam
'''

def sortsol(solution):
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
                sol3[j] = sol3[j+1]
                sol[j + 1] = temp
                sol3[j+1] = temp2
            if sol[j].time < sol[j+1].time and sol[j].date == sol[j+1].date:
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

def print_solution(sol):
    for i in sol.keys():
        print(i, " ", sol[i].room, " ", sol[i].teacher, " ", sol[i].date, " ", sol[i].time)

def returnSoftConstraintTwoAndThree(examSchedule):
    global studentEnrolledCourses
    examSchedule = sortsol(examSchedule)
    # print_solution(examSchedule)    
    # exam, schedule = examSchedule.items()
    # print(schedule)
    # var = sorted(examSchedule.items(), lambda x,key=lambda y: y.date)
    # print(var)
    costOfCSCourseOverMGCourse = 0
    costOfConsecutiveExams = 0
    for student, coursesList in studentEnrolledCourses.items():
        examOccured = False
        checkCSCourseInFirstSlot = False
        for course in coursesList:
            for exam in examSchedule.keys():
                # print(schedule)
                if(examSchedule[exam].time == 9): # First check exams of the student in first slot
                    if(course == exam):
                        examOccured = True
                        if("CS" in course):
                            checkCSCourseInFirstSlot = True
                else:
                    if(course == exam):
                        # print(examOccured)
                        if(examOccured): # Then check exams of the student in 2nd slot
                            print(1)
                            costOfConsecutiveExams+=1
                        if("MG" in course and checkCSCourseInFirstSlot):
                            print(2)
                            costOfCSCourseOverMGCourse+=1
                        checkCSCourseInFirstSlot = False
                        examOccured = False
    return costOfConsecutiveExams, costOfCSCourseOverMGCourse


def costfunction(sol):
    cost = 0
    costOfConsecutiveExams, costOfCSCourseOverMGCourse = returnSoftConstraintTwoAndThree(sol)
    if studentconstraint(sol):
        cost = cost + 10
    if teachersconstraint(sol):
        cost = cost + 10
    if costOfConsecutiveExams:
        cost += 5
    if costOfCSCourseOverMGCourse:
        cost += 5
    return cost


def getclashes(sol):
    date_list = []
    for student in indstudentcourses.keys():
        for course in indstudentcourses[student]:
            date_list.append(sol[course].date)
        a = set(date_list)
        if len(a) != len(date_list):
            return student
        date_list = []
    return False


def neighboringsolution(solution):
    student = getclashes(solution)
    if not student:
        date1 = 0
        date2 = 0
        while date1 == date2:
            index1 = random.randint(0, len(solution.items()) - 1)
            index2 = random.randint(0, len(solution.items()) - 1)
            if index1 == index2:
                continue
            date1 = list(solution.values())[index1].date
            date2 = list(solution.values())[index2].date
            if date1 == date2:
                continue
            course1 = list(solution.keys())[index1]
            course2 = list(solution.keys())[index2]
            solution[course1].date = date2
            solution[course2].date = date1
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


def setupdata():
    importdata()
    assignstudentstocourse()
    assigncourses()


def simulatedanealing():
    temp = 1000
    coolingrate = 1
    currentsol = random_solution()
    bestsol = random_solution()
    currentcost = costfunction(currentsol)
    bestcost = currentcost
    while temp > 1:
        load = "*" * (100 - int(temp / 10)) + "_" * int(temp / 10)
        prGreen("[" + str(load) + "]\n")
        newsol = copy.deepcopy(neighboringsolution(currentsol))
        newcost = costfunction(newsol)
        prYellow("Current Cost: " + str(newcost) + '\n')
        if newcost > currentcost:
            currentsol = newsol
            currentcost = newcost
            bestsol = copy.deepcopy(newsol)
            bestcost = newcost
            if newcost == 30:
                break
        else:
            costdiff = newcost - currentcost
            if random.uniform(0, 1) < math.exp(-costdiff / temp):
                currentsol = newsol
                currentcost = newcost
        temp = temp - coolingrate
    #     clear()
    # clear()
    testFunction(bestsol)
    # print(bestsol)
    return createtable(bestsol)


def setday(datalist):
    day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    dt = copy.deepcopy(datalist)
    dy = []
    for i in range(len(dt)):
        dy.append('')
    j = dt[0] - 1
    for i in range(len(dt)):
        if(j > 4):
            j = dt[0] - 1
        dy[i] = day[j]
        if i != len(dt)-1 and dt[i+1] > dt[i]:
            j = j+1
    return dy



def createdataframe(bestsol):
    result = []
    for i in bestsol:
        result.append([])

    for i in range(len(bestsol)):
        for j in range(len(bestsol[0])):
            result[j].append(bestsol[i][j])
    df = pd.DataFrame(bestsol, columns=["Course Code", "Room Number", "Teacher Name", "Date", "Time Slot"])
    sdf = df.sort_values(by=['Date', 'Time Slot'], ascending=True)
    daycol = setday(list(sdf['Date']))
    # print(daycol)
    sdf['Day'] = daycol
    if os.path.exists('Datesheet.csv'):
        os.remove('Datesheet.csv')

    sdf.to_csv('Datesheet.csv')
    return sdf

# Remove duplicates from a dictionary
def removeDuplicates(myList):
    return list(dict.fromkeys(myList))

def testFunction(bestsol):
    global courses
    listOfexams = []
    # for exam in bestsol:
    #     listOfexams.append(exam)
    
    # print(courses)
    # print('\n' + str(len(courses)) + '\n')
    # for course in courses:
    #     print(course)
    # listOfexams = removeDuplicates(listOfexams)
    # print('\n' + str(len(listOfexams)) + '\n')

prPurple("Press 1 for 2 week Schedule\n Press 2 for 3 Week Schedule\n")
x = int(input("Enter Option: "))
if x == 1:
    days = 10
else:
    days = 15
setupdata()
print(createdataframe(simulatedanealing()))
x = input("Press any key to exit")