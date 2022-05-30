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
        if(round(decimalValue) != 0 or floatValue != 0):
            i+=1
            if(i>totalCapcityOfARoom):
                reserveExamList.append((courseCode))
            else:
                fullRooms.append((courseCode, i))
    return fullRooms


''' Functions for accurate calculation to assign rooms for students '''
# def convertEnrolledStudentsToRooms(result):
#     partialRooms = []
#     fullRooms = []
#     totalCapcityOfARoom = returnRoomCapacityOfARoom()
#     for courseCode, capacity in result:
#         tempCapacity = capacity/totalCapcityOfARoom
#         floatValue, decimalValue = math.modf(tempCapacity)
#         # print(courseCode, tempCapacity ,decimalValue, floatValue)
#         if(round(decimalValue) != 0):
#             fullRooms.append((courseCode, decimalValue))
#         if(floatValue != 0):
#             partialRooms.append((courseCode, floatValue))
#     return partialRooms, fullRooms

# def insertForFullValues(fullRooms, table, i):
#     for courseCode, capacity in fullRooms:
#         for roomNumber in range(int(capacity)):
#             table.append([courseCode, i+1])
#             i+=1
#     return fullRooms, table, i

# def readjustRoomNumbersOfTable(table, start):
#     global numberOfRooms
#     i = len(table)-1
#     listOfRooms = [x[1] for x in table]
#     if(len(table) <= 0):
#         return table
#     if(table[i][1] > numberOfRooms):
#         while(i != 0):
#             j = start
#             courseCode, roomNumber = table[i]
#             # print((courseCode, roomNumber))
#             if(roomNumber > numberOfRooms):
#                 while(j != i):
#                     if j not in listOfRooms:
#                         table.remove([courseCode, roomNumber])
#                         table.append([courseCode, j])
#                         break
#                     j+=1
#             else:
#                 break
#             i-=1
#     table.sort(key=lambda s: s[1])
#     return table

# def insertForPartialValues(partialRooms, table, i):
#     sum = 0
#     partialCourseList = []
#     for courseCode, capacity in partialRooms:
#         partialCourseList.append((courseCode, capacity))
#         sum+=capacity
#         if((sum > 1)): # For Multiple Class Rooms
#             # partialCourseList.sort(key=lambda s: s[1])
#             i+=1
#             for courseCode2, capacity2 in partialCourseList:
#                 table.append([courseCode2, i+1])
#             partialCourseList = []
#             i+=1
#             table.append([courseCode, i+1])
#             sum = 0
#         elif((sum >=0.9) and (sum) <= 1): # For just a single classroom
#             sum = 0
#             i+=1
#             for courseCode2, capacity2 in partialCourseList:
#                 table.append([courseCode2, i+1])
#             partialCourseList= []
#     return partialRooms, table, i


def assignRoomTeacherAndTimeForAShift(result):
    global studentsLimit, examSchedule
    table = []
    time, date = returnTimeAndDate()
    teachers = returnTeachersForAShift(determineShift(time))
    fullRooms = convertStudentsToRooms(result)
    # partialRooms, fullRooms = convertEnrolledStudentsToRooms(result)
    # partialRooms.sort(key=lambda s: s[1])
    fullRooms.sort(key=lambda s: s[1])
    print(fullRooms)
    # print(teachers)
    i = 0
    # For Full Rooms
    # fullRooms, table, i = insertForFullValues(fullRooms, table, i)
    # For Half or less capacity rooms
    # partialRooms, table, i = insertForPartialValues(partialRooms, table, i)
    # print("Fully Filled Rooms: " + str(fullRooms))
    # print("Partial Filled Rooms: " + str(partialRooms))
    # print("Resultant Table: "+ str(table))
    # table = readjustRoomNumbersOfTable(table, len(fullRooms))
    # print(teachers)
    # if(len(table) <= 0):
    #     return
    # for exam in table:
    #     # print(exam[1])
    #     exam.append(teachers[(exam[1]-1)])
    #     exam.append(time)
    #     exam.append(date)
    # if(determineShift(time) == 1):
    #     importRandomTeachersForADay() # This imports new teachers for a day
    # examSchedule.append(table)
    # print("Resultant Table: "+ str(table))

def removeExamFromResult(result):
    global reserveExamList
    reservedExam = result[0]
    reserveExamList.append(reservedExam)
    result.remove(reservedExam)
    return result

def removeDuplicates(myList):
    return list(dict.fromkeys(myList))

def createCombination(exam, remainingExamsList):
    global studentsLimit
    result = []
    totalSum = exam[1]
    result.append(exam)
    random.shuffle(remainingExamsList)
    for exam in remainingExamsList:
        if( (totalSum+exam[1]) <= studentsLimit):
            totalSum += exam[1]
            result.append(exam)
            remainingExamsList.remove(exam)
    result = removeExamFromResult(result)
    assignRoomTeacherAndTimeForAShift(result)
    return remainingExamsList

def computeSchedule():
    global examSchedule, reserveExamList
    # global table
    importRandomTeachersForADay()
    exam, remainingExamsList = randomlyPickExamAndReturnListOfExams(convertDictionaryToList(countCourseRegisteredStudents))
    remainingExamsList = createCombination(exam, remainingExamsList)
    print(examSchedule)
    # print(table)
    # while(len(remainingExamsList) > 0):
    #     remainingExamsList = createCombination(exam, remainingExamsList)
    # reserveExamList = removeDuplicates(reserveExamList)
    # print(reserveExamList)
    # # while(len(reserveExamList) > 0):
    # reserveExamList = createCombination(exam, reserveExamList)
    # print(reserveExamList)

    # print(examSchedule)
    # print("Resultant Table"+ str(table))
    

importFiles()
setVariables()
computeSchedule()