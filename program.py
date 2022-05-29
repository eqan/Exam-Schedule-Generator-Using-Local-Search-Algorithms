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

def insertForFullValues(fullRooms, table, i):
    for courseCode, capacity in fullRooms:
        for roomNumber in range(int(capacity)):
            table.append((courseCode, i+1))
            i+=1
    return fullRooms, table, i

def insertForPartialValues(partialRooms, table, i):
    sum = 0
    partialCourseList = []
    for courseCode, capacity in partialRooms:
        if((sum+capacity >=1)): # For Multiple Class Rooms
            sum = 0
            if(len(partialCourseList) > 0):
                i+=1
                for courseCode2, capacity2 in partialCourseList:
                    table.append((courseCode2, i+1))
            i+=1
            if(capacity > 0.85):
                table.append((courseCode, i+1))
            partialCourseList = []
        elif((sum+capacity >=0.9) and (sum+capacity) <= 1): # For just a single classroom
            sum = 0
            i+=1
            for courseCode2, capacity2 in partialCourseList:
                table.append((courseCode2, i+1))
            partialCourseList= []

        partialCourseList.append((courseCode, capacity))
        sum+=capacity
    if(len(partialCourseList) > 0):
        for courseCode2, capacity2 in partialCourseList:
            table.append((courseCode2, i+1))
    return sum , partialRooms, table, i


    # partialCourseList = []
    # for courseCode, capacity in partialRooms:
    #     partialRooms.remove((courseCode, capacity))
    #     sum+=capacity
    #     if(sum >=0.9 and sum <= 1): # For just a single classroom
    #         for courseCode, capacity in partialCourseList:
    #             table.append((courseCode, i+1))
    #         partialCourseList = []
    #         sum = 0
    #         i+=1
    #     elif(sum > 1): # For assigning multiple classrooms
    #         partialCourseList.sort(key=lambda s: s[1], reverse=True)
    #         for courseCode, capacity in partialCourseList:
    #             if(sum > 1):
    #                 table.append((courseCode, i+1))
    #                 sum -=capacity
    #                 i+=1
    #             else:
    #                 table.append((courseCode, i+1))
    #         partialCourseList = []
    #         sum = 0
    #         i+=1
    #     partialCourseList.append((courseCode, capacity))

    # print("Partial Filled Rooms: " + str(partialRooms))
    # # print("Resultant Table"+ str(table))
    # # print(partialRooms)
    # if(len(partialRooms) > 0):
    #     insertForPartialValues(sum, partialRooms, table, i)
    # else:
    #     for courseCode, capacity in partialCourseList:
    #         table.append((courseCode, i+1))

    # return sum , partialRooms, table, i


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
    fullRooms, table, i = insertForFullValues(fullRooms, table, i)
    # For Half or less capacity rooms
    # print(teachers)
    # print("Partial Filled Rooms: " + str(partialRooms))
    sum , partialRooms, table, i = insertForPartialValues(partialRooms, table, i)
    # print("Partial Filled Rooms: " + str(partialRooms))
    # while(len(partialRooms) > 0):
    # sum , partialRooms, table, date, time, teachers, i = insertForPartialValues(0, partialRooms, table, date, time, teachers, i)
    #     print("Partial Filled Rooms: " + str(partialRooms))
    #     try:
    #         if(len(partialRooms) == 1):
    #             # # for courseCode, capacity in partialRooms:
    #             # #     if(sum > 1):
    #             #         table.append((date, time, courseCode, teachers[i], i+1))
    #             #         table.append((date, time, courseCode, teachers[i+1], i+2))
    #             #         i+=2
    #             #     else:
    #             table.append((date, time, courseCode, teachers[i], i+1))
    #                 # partialRooms.remove((courseCode,capacity))
    #         else:
    #             sum , partialRooms, table, date, time, teachers, i = insertForPartialValues(sum, partialRooms, table, date, time, teachers, i)
    #             print(table)
    #     except:
    #         print("Couldnt iterate over teachers")
    #         break
    #         # i-=1
    # print(studentsLimit)
    print("Resultant Table"+ str(table))

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

importFiles()
setVariables()
exam, remainingExamsList = randomlyPickExamAndReturnListOfExams(convertDictionaryToList(countCourseRegisteredStudents))
createCombination(exam, remainingExamsList)