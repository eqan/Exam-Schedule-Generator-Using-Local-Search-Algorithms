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

def computeSchedule():
    global examSchedule, reserveExamList, countCourseRegisteredStudents
    # global table
    # print(countCourseRegisteredStudents)
    importRandomTeachersForADay()
    remainingExamsList = convertDictionaryToList(countCourseRegisteredStudents)
    remainingExamsList = createCombination(remainingExamsList)
    while(len(remainingExamsList) > 0):
        remainingExamsList = createCombination(remainingExamsList)
    print(examSchedule)
    

importFiles()
setVariables()
computeSchedule()