import pandas as pd
import matplotlib.pyplot as plt
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
availableRooms, availableTeachers = [], []

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
    availableTeachers = availableTeachers[:numberOfRooms]

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

def resetDataForNextDay():
    return 1

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
        resetDataForNextDay()

    return assignTimeStamp, assignDate

def returnTeachersForAShift(shift):
    global availableTeachers, numberOfRooms
    fullDayCapacity = numberOfRooms*2
    if(shift == 0):
        return availableTeachers[:fullDayCapacity]
    return availableTeachers[fullDayCapacity:]

def returnRoomCapacityOfARoom():
    global rooms
    return rooms.iloc[0]['Capacity']

def convertEnrolledStudentsToRooms(result):
    partialRooms = []
    fullRooms = []
    totalCapcityOfARoom = returnRoomCapacityOfARoom()
    for courseCode, capacity in result:
        tempCapacity = capacity/totalCapcityOfARoom
        floatValue, decimalValue = math.modf(tempCapacity)
        # print(courseCode, tempCapacity ,decimalValue, floatValue)
        if(round(decimalValue) != 0):
            fullRooms.append((courseCode, decimalValue))
        if(floatValue != 0):
            partialRooms.append((courseCode, floatValue))
    return partialRooms, fullRooms

def insertForPartialValues(sum , partialRooms, table, date, time, teachers, i):
    partialCourseList = []
    for courseCode, capacity in partialRooms:
        if (courseCode, capacity) in partialRooms:
            partialRooms.remove((courseCode,capacity))
        else:
            print("Not Found" + str((courseCode, capacity)))
        sum+=capacity
        if(sum >=0.85):
            for courseCode, capacity in partialCourseList:
                table.append((date, time, courseCode, teachers[i], i+1))
            i+=1
            partialCourseList = []
            sum = 0
        partialCourseList.append((courseCode, capacity))
    return sum , partialRooms, table, date, time, teachers, i


def assignRoomTeacherAndTimeForAShift(result):
    global studentsLimit
    table = []
    time, date = returnTimeAndDate()
    teachers = returnTeachersForAShift(determineShift(time))
    partialRooms, fullRooms = convertEnrolledStudentsToRooms(result)
    partialRooms.sort(key=lambda s: s[1])
    fullRooms.sort(key=lambda s: s[1])
    # print(teachers)
    print("Fully Filled Rooms: " + str(fullRooms))
    print("Partial Filled Rooms: " + str(partialRooms))
    i = 0
    # For Full Rooms
    for courseCode, capacity in fullRooms:
        for roomNumber in range(int(capacity)):
            table.append((date, time, courseCode, teachers[i], i+1))
            i+=1
    # j = i
    # For Half or less capacity rooms
    print(teachers)
    print("Partial Filled Rooms: " + str(partialRooms))
    sum , partialRooms, table, date, time, teachers, i = insertForPartialValues(0, partialRooms, table, date, time, teachers, i)
    while(len(partialRooms) > 0):
        print("Partial Filled Rooms: " + str(partialRooms))
        try:
            if(len(partialRooms) == 1):
                for courseCode, capacity in partialRooms:
                    if(sum > 1):
                        table.append((date, time, courseCode, teachers[i], i+1))
                        table.append((date, time, courseCode, teachers[i+1], i+2))
                        i+=2
                    else:
                        table.append((date, time, courseCode, teachers[i], i+1))
                    partialRooms.remove((courseCode,capacity))
            else:
                sum , partialRooms, table, date, time, teachers, i = insertForPartialValues(sum, partialRooms, table, date, time, teachers, i)
        except:
            print("Couldnt iterate over teachers")
            i-=1
    print(studentsLimit)
    print(table)
    # print(table2)

def createCombination(exam, remainingExamsList):
    global studentsLimit
    importRandomTeachersForADay()
    result = []
    totalSum = exam[1]
    result.append(exam)
    random.shuffle(remainingExamsList)
    for exam in remainingExamsList:
        if( (totalSum+exam[1]) <= studentsLimit):
            totalSum += exam[1]
            result.append(exam)
            remainingExamsList.remove(exam)
    assignRoomTeacherAndTimeForAShift(result)

def create_dataframe(examlist):
    td = dict(examlist)
    temp_list = list(td.keys())
    temp_matrix=[]
    x = 0
    while x < len(temp_list)-1:
        temp_row = []
        temp_row.append(temp_list[x])
        n = courses['Course Name'].where(courses['Course Code'] == temp_list[x])
        temp_row.append(list(n.dropna())[0])
        temp_row.append(temp_list[x+1])
        n = courses['Course Name'].where(courses['Course Code'] == temp_list[x+1])
        temp_row.append(list(n.dropna())[0])
        temp_matrix.append(temp_row)
        x=x+1

    df = pd.DataFrame(temp_matrix,columns=['9:00 - 12:00', 'Course Name', '1:00 - 4:00', 'Course Name'])
    pd.set_option('display.max_columns', None)
    return df

importFiles()
setVariables()
exam, remainingExamsList = randomlyPickExamAndReturnListOfExams(convertDictionaryToList(countCourseRegisteredStudents))
# print(exam)
# print(remainingExamsList)
# exam = ('JK123', 23)
# remainingExamsList = [('Pk', 30), ('LI', 50),  ('MNA', 20)]
createCombination(exam, remainingExamsList)