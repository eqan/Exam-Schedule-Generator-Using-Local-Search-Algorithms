import copy
import pandas as pd
import numpy as np
import os
import csv
import random
import math
import time

courses, rooms, studentCourses, studentNames, teachers = [], [], [], [], []
countCourseRegisteredStudents = {}
studentsLimit, numberOfRooms  = 0, 0
currentDate = {'shift': 0, 'day': 0} #Hour Shift , Day 
availableTeachers = []
reserveExamList = []
examSchedule = []

fileDir = './actual_dataset/'


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def importFiles():
    global courses, rooms, studentCourses, studentNames, teachers
    courses = pd.read_csv(fileDir + 'courses.csv')
    rooms = pd.read_csv(fileDir + 'rooms.csv')
    studentCourses = pd.read_csv(fileDir +'studentCourses.csv')
    studentNames = pd.read_csv(fileDir +'studentNames.csv')
    teachers = pd.read_csv(fileDir +'teachers.csv')


def countStudentsInCourse():
    global studentCourses, courses, countCourseRegisteredStudents
    for i, j, studentNameSC, courseCodeSC in studentCourses.itertuples():
        for i, courseCodeC, courseNameC in courses.itertuples():
            if(courseCodeC == courseCodeSC):
                if courseCodeC not in countCourseRegisteredStudents:
                    countCourseRegisteredStudents[courseCodeC] = 0
                else:
                    countCourseRegisteredStudents[courseCodeC] +=1


def importRandomTeachersForADay():
    global teachers, numberOfRooms, availableTeachers
    availableTeachers = teachers['Teacher Name'].tolist()
    random.shuffle(availableTeachers)
    availableTeachers = availableTeachers[:numberOfRooms*2]


def calculateStudentsLimitInRooms():
    global studentsLimit
    for i, roomNumber, capacity in rooms.itertuples():
        studentsLimit += int(capacity)


def setVariables():
    global rooms, numberOfRooms
    numberOfRooms = len(rooms.index)
    countStudentsInCourse()
    calculateStudentsLimitInRooms()


def convertDictionaryToList(input):
    return list(input.items())


def randomlyPickExamAndReturnListOfExams(entry_list):
    exam = random.choice(entry_list)
    entry_list.remove(exam)
    return exam, entry_list


def determineShift(time):
    if(time == 9):
        return 0
    return 1


def returnTimeAndDate():
    global currentDate
    assignTimeStamp = 0
    assignDate = currentDate['day']
    if(currentDate['shift'] == 0):
        assignTimeStamp = 9
        currentDate['shift'] = 1
    else:
        assignTimeStamp = 2
        currentDate['shift'] = 0
        currentDate['day'] += 1
    return assignTimeStamp, assignDate


def returnTeachersForAShift(shift):
    global availableTeachers, numberOfRooms
    fullDayCapacity = numberOfRooms
    if(shift == 0):
        return availableTeachers[:fullDayCapacity]
    return availableTeachers[fullDayCapacity:]


def returnRoomCapacityOfARoom():
    global rooms
    return rooms.iloc[0]['Capacity']


def convertStudentsToRooms(result):
    global reserveExamList
    fullRooms = []
    totalCapcityOfARoom = returnRoomCapacityOfARoom()
    i= 0
    for courseCode, capacity in result:
        tempCapacity = capacity/totalCapcityOfARoom
        floatValue, decimalValue = math.modf(tempCapacity)
        # print(courseCode, tempCapacity ,decimalValue, floatValue)
        if(int(decimalValue) != 0):
            for j in range(int(decimalValue)):
                fullRooms.append([courseCode, i+j])
            i+=int(decimalValue)
        if(floatValue != 0):
            fullRooms.append([courseCode, i])
            i+=1
    return fullRooms


def assignRoomTeacherAndTimeForAShift(result):
    global studentsLimit, examSchedule, numberOfRooms
    table, reserveExamList = [], []
    time, date = returnTimeAndDate()
    teachers = returnTeachersForAShift(determineShift(time))
    table = convertStudentsToRooms(result)
    temporaryList =0
    # partialRooms, fullRooms = convertEnrolledStudentsToRooms(result)
    # partialRooms.sort(key=lambda s: s[1])
    if(len(table) <= 0):
        return 
    for exam in table:
        # print(exam)
        if((exam[1]) >= numberOfRooms):
            # print(exam)
            newRoomNumber = exam[1] - numberOfRooms
            reserveExamList.append([exam[0], newRoomNumber])
            table.remove(exam)
        else:
            teacher = teachers[(exam[1]-1)]
            exam.append(teacher)
            exam.append(time)
            exam.append(date)
    # print(table)
    temporaryList = (list(filter(lambda tup : len(tup) == 2, table)))
    # print(temporaryList)
    table = list(filter(lambda tup : len(tup) != 2, table))
    # print(table)
    if(len(temporaryList) > 0):
        for exam in temporaryList:
            newRoomNumber = exam[1] - numberOfRooms
            reserveExamList.append([exam[0], newRoomNumber])

    examSchedule.append(table)
    if(len(reserveExamList) > 0):
        time, date = returnTimeAndDate()
        for exam in reserveExamList:
            if(len(exam) > 0):
                # print(exam)
                exam.append(teachers[(exam[1]-1)])
                exam.append(time)
                exam.append(date)
        examSchedule.append(reserveExamList)
    if(determineShift(time) == 1):
        importRandomTeachersForADay() # This imports new teachers for a day


def removeDuplicates(myList):
    return list(dict.fromkeys(myList))


def createCombination(remainingExamsList):
    global studentsLimit
    result = []
    totalSum = 0
    random.shuffle(remainingExamsList)
    for exam in remainingExamsList:
        if(totalSum <= studentsLimit):
            totalSum += exam[1]
            result.append(exam)
            remainingExamsList.remove(exam)
    assignRoomTeacherAndTimeForAShift(result)
    return remainingExamsList


def testExamSchedule():
    global examSchedule
    testDict = {}
    for schedule in examSchedule:
        for exam in schedule:
            # print(exam)
            courseCode = exam[0]
            if courseCode not in testDict:
                testDict[courseCode] = 1
            else:
                testDict[courseCode] +=1
    print(testDict)


def groupstudents():
    td = list(studentCourses['Course Code'])
    tid = list(studentCourses['Student Name'])
    coursestudents = {}
    for i in td:
        coursestudents[i] = []
    for i in td:
        n = studentCourses['Student Name'].where(studentCourses['Course Code'] == i)
        td = list(n.dropna())
        coursestudents[i] = td
    return coursestudents


def groupcourses():
    td = list(studentCourses['Course Code'])
    tid = list(studentCourses['Student Name'])
    studentcourse = {}
    for i in tid:
        studentcourse[i] = []
        n = studentCourses['Course Code'].where(studentCourses['Student Name'] == i)
        tx = list(n.dropna())
        studentcourse[i] = tx
    for i in studentcourse:
        if len(studentcourse[i]) < 3:
            studentcourse.pop(i)
    return studentcourse


def studentcheck(examschedule, studentcourse):
    templist = copy.deepcopy(examschedule)
    flag = False
    x = 0
    for i in templist:
        for j in templist:
            if i[0] != j[0] and i[0] in studentcourse and j[0] in studentcourse:
                if i[len(i) - 1] == j[len(j) - 1] and i[len(i) - 2] == j[len(j) - 2]:
                    flag = True
                    if i in templist and j in templist:
                        templist.remove(i)
                        templist.remove(j)
    return flag


def computeSchedule():
    global examSchedule, reserveExamList, countCourseRegisteredStudents
    # global table
    # print(countCourseRegisteredStudents)
    importRandomTeachersForADay()
    remainingExamsList = convertDictionaryToList(countCourseRegisteredStudents)
    remainingExamsList = createCombination(remainingExamsList)
    while(len(remainingExamsList) > 0):
        remainingExamsList = createCombination(remainingExamsList)


def costfunction(examsch):
    temp = examsch
    cost = 0
    st = groupcourses()
    key = list(st.keys())
    for i in key:
        if studentcheck(temp, st[i]):
            cost = cost + 1
    return cost


def newsolution(examsch):
    exams = copy.deepcopy(examsch)
    timing = []
    for i in exams:
        timing.append(i[len(i)-1])
    mt = max(timing)
    temp = random.choice(exams)
    examday = random.randint(0, mt)
    temp2 = []
    for i in exams:
        if i[len(i)-1] == examday and i[1] == temp[1] and i[0] != temp[0]:
            temp2 = i
            i = temp
            i[len(i)-1] = examday
            temp2[4] = examday+1
            exams.append(temp2)
    return exams


def normalizesol(examSchedule):
    randomsol = []
    for i in range(len(examSchedule)):
        for j in range(len(examSchedule[i])):
            randomsol.append(examSchedule[i][j])
    return randomsol


def swapDateAndTime(examToBeDiscarded, examToBeAssignedNewValue):
    exam1Time = examToBeDiscarded[3]
    exam1Date = examToBeDiscarded[4]
    exam2Time = examToBeAssignedNewValue[3]
    exam2Date = examToBeAssignedNewValue[4]
    examToBeAssignedNewValue[3] = exam1Time
    examToBeAssignedNewValue[4] = exam1Date
    return examToBeAssignedNewValue


def swapMGExamsWithCSExams(schedule, csExamsInFirstSlot, mgExamsInSecondSlot):
    if (len(csExamsInFirstSlot) <= 0 or len(mgExamsInSecondSlot) <= 0):
        return examSchedule
    localCopyOfCsExams = copy.deepcopy(csExamsInFirstSlot)
    localCopyOfMgExams = copy.deepcopy(mgExamsInSecondSlot)
    i = 0
    for exam in schedule:
        if (i == 0):
            for csExam in csExamsInFirstSlot:
                if (csExam == exam):
                    if (len(localCopyOfMgExams) > 0):
                        schedule.remove(exam)
                        mgExam = localCopyOfMgExams.pop()
                        schedule.append(swapDateAndTime(mgExam, csExam))
            i += 1
        else:
            for mgExam in mgExamsInSecondSlot:
                if (mgExam == exam):
                    if (len(localCopyOfCsExams) > 0):
                        schedule.remove(exam)
                        csExam = localCopyOfCsExams.pop()
                        schedule.append(swapDateAndTime(csExam, mgExam))
            i = 0
    return schedule


def priortizeCSCourseOverMGCourse(schedule):
    csExamsInFirstSlot = []
    mgExamsInSecondSlot = []
    for student, coursesList in groupcourses().items():
        checkCSCourseInFirstSlot = False
        for course in coursesList:
            i = 0
            for exam in schedule:
                if(i == 0):
                    if(course == exam[0]): # First check exams of the student in first slot
                        if("CS" in course):
                            if(exam not in csExamsInFirstSlot):
                                csExamsInFirstSlot.append(exam)
                            checkCSCourseInFirstSlot = True
                else:
                    if(course == exam[0]): # Then check exams of the student in 2nd slot
                        if("MG" in course and checkCSCourseInFirstSlot):
                            if(exam not in mgExamsInSecondSlot):
                                mgExamsInSecondSlot.append(exam)
                        checkCSCourseInFirstSlot = False
            if(i == 0):
                i+=1
            else:
                i=0
    # csExamsInSecondSlot = removeDuplicates(csExamsInSecondSlot)
    return(swapMGExamsWithCSExams(schedule, csExamsInFirstSlot, mgExamsInSecondSlot))


def simulatedanealing():
    global examSchedule
    temp = 100
    coolingrate = 4
    computeSchedule()
    rand = normalizesol(examSchedule)
    currentsol = copy.deepcopy(rand)
    bestsol = copy.deepcopy(rand)
    currentcost = costfunction(currentsol)
    bestcost = currentcost
    while temp > 1:
        newsol = newsolution(currentsol)
        newcost = costfunction(newsol)
        if newcost <= currentcost:
            currentsol = newsol
            currentcost = newcost
            bestsol = normalizesol(priortizeCSCourseOverMGCourse(newsol))
            bestcost = newcost
            if newcost == 0:
                break
        else:
            costdiff = newcost - currentcost
            if random.uniform(0, 1) < math.exp(-costdiff / temp):
                currentsol = newsol
                currentcost = newcost
        temp = temp - coolingrate
        clear()
        load = "*"*(100-temp) + "_"*temp
        print("[", load, "]")
    clear()
    return sortsol(bestsol)


def sortsol(solution):
    sol = copy.deepcopy(solution)
    for i in range(len(sol)):

        # loop to compare array elements
        for j in range(0, len(sol) - i - 1):

            # compare two adjacent elements
            # change > to < to sort in descending order
            if sol[j][4] > sol[j + 1][4]:
                # swapping elements if elements
                # are not in the intended order
                temp = sol[j]
                sol[j] = sol[j + 1]
                sol[j + 1] = temp
    return sol


def createdataframe(bestsol):
    result = []
    for i in bestsol:
        result.append([])

    for i in range(len(bestsol)):
        for j in range(len(bestsol[0])):
            result[j].append(bestsol[i][j])
    df = pd.DataFrame(bestsol, columns=["Course Code", "Room Number", "Teacher Name", "Time Slot", "Date"])
    df.to_csv('Datesheet.csv')
    return df


importFiles()
setVariables()
print(createdataframe(simulatedanealing()))
k = input("Press any key to exit")