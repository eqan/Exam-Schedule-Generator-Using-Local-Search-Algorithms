import pandas as pd
import numpy as np
import os
import csv
import random
import math
import time

# Variables to store imported data
courses, rooms, studentCourses, studentNames, teachers = [], [], [], [], []
# Variables to store student enrolled in courses and vice versa
studentEnrolledCourses, courseEnrolledStudents = {}, {}
# count the total registered students of each course
countCourseRegisteredStudents = {}
# Count the total students that have MG course over a CS course in a day and vice versa
countStudentHavingMGCourseBeforeCSCourse, countStudentHavingCSCourseBeforeMGCourse = 0, 0
# Count students limit and number of rooms
studentsLimit, numberOfRooms  = 0, 0
# Store the current shift and day for a course
currentDate = {'shift': 0, 'day': 0} #Hour Shift , Day 
# Store the available teachers for a day
availableTeachers = []
# Store the resultant exam schedule
examSchedule = []

# File directory variables
fileDir = './test_dataset/'
# fileDir = './actual_dataset/'

# Import files function to imporat all the data from files to variables
def importFiles():
    global courses, rooms, studentCourses, studentNames, teachers, studentCourses, coursesStudents
    courses = pd.read_csv(fileDir + 'courses.csv')
    rooms = pd.read_csv(fileDir + 'rooms.csv')
    studentCourses = pd.read_csv(fileDir +'studentCourses.csv')
    studentNames = pd.read_csv(fileDir +'studentNames.csv')
    teachers = pd.read_csv(fileDir +'teachers.csv')

# Group students according to courses
def groupstudents():
    global courseEnrolledStudents
    td = list(studentCourses['Course Code'])
    tid = list(studentCourses['Student Name'])
    for i in td:
        courseEnrolledStudents[i] = []
    for i in td:
        n = studentCourses['Student Name'].where(studentCourses['Course Code'] == i)
        td = list(n.dropna())
        courseEnrolledStudents[i] = td

# Group courses according to students
def groupcourses():
    global studentEnrolledCourses
    td = list(studentCourses['Course Code'])
    tid = list(studentCourses['Student Name'])
    studentEnrolledCourses = {}
    for i in tid:
        studentEnrolledCourses[i] = []
        n = studentCourses['Course Code'].where(studentCourses['Student Name'] == i)
        tx = list(n.dropna())
        studentEnrolledCourses[i] = tx
    for i in studentEnrolledCourses:
        if len(studentEnrolledCourses[i]) < 3:
            studentEnrolledCourses.pop(i)


def initializeVariables():
    global rooms, numberOfRooms
    importFiles()
    groupstudents()
    groupcourses()
    numberOfRooms = len(rooms.index)
    countStudentsInCourse()
    calculateStudentsLimitInRooms()

# Count students enrolled in a course
def countStudentsInCourse():
    global studentCourses, courses, countCourseRegisteredStudents
    for i, j, studentNameSC, courseCodeSC in studentCourses.itertuples():
        for i, courseCodeC, courseNameC in courses.itertuples():
            if(courseCodeC == courseCodeSC):
                if courseCodeC not in countCourseRegisteredStudents:
                    countCourseRegisteredStudents[courseCodeC] = 0
                else:
                    countCourseRegisteredStudents[courseCodeC] +=1

# Import random teachers for a day
def importRandomTeachersForADay():
    global teachers, numberOfRooms, availableTeachers
    availableTeachers = teachers['Teacher Name'].tolist()
    random.shuffle(availableTeachers)
    availableTeachers = availableTeachers[:numberOfRooms*2]

# Calculate the students limit in a room
def calculateStudentsLimitInRooms():
    global studentsLimit
    for i, roomNumber, capacity in rooms.itertuples():
        studentsLimit += int(capacity)

# Convert a dictionary to a list
def convertDictionaryToList(input):
    return list(input.items())

# Return Shift of the day according to time
def determineShift(time):
    if(time == 9):
        return 0
    return 1

# Return time and date and update for the next day and shift
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

# Return teachers for a shift
def returnTeachersForAShift(shift):
    global availableTeachers, numberOfRooms
    fullDayCapacity = numberOfRooms
    if(shift == 0):
        return availableTeachers[:fullDayCapacity]
    return availableTeachers[fullDayCapacity:]

# Return room capacity
def returnRoomCapacityOfARoom():
    global rooms
    return rooms.iloc[0]['Capacity']

# Convert the number of students to number of rooms
def convertStudentsToRooms(result):
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

# Assign a room, teacher and time for a shift
def assignRoomTeacherAndTimeForAShift(result):
    global studentsLimit, examSchedule, numberOfRooms
    table, reserveExamList = [], []
    time, date = returnTimeAndDate()
    teachers = returnTeachersForAShift(determineShift(time))
    table = convertStudentsToRooms(result)
    temporaryList =0
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

# Remove duplicates from a dictionary
def removeDuplicates(myList):
    return list(dict.fromkeys(myList))

# Create a combination for shift
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

# Just for testing the exam schedule
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

''' 
Soft Constraint #2: A student shall not give more than 1 exam consecutively.
Day 1  = Prob Pak

Day 13 no consecutive
Comm LA

Prob Comm
La Pak

check_consecutive_exams(result):
	if(threat(result)  == 0)
		return result
	day1 = Konsa din consecutive exams
	day2 = No consecutive exams
	result  = swap(1 Course of day1, 1 course of day2)
	check_consecutive_exams(result)

'''
def checkConsecutiveExams():

    return 1

''' 
Soft Constraint#3: If a student is enrolled in a MG course and a CS course, it is preferred that their MG course
 exam be held before their CS course exam
'''
# A function that computes the ration of students having CS exams over MG
def computeCSAndMGCourseAlignmentForADayRatio():
    global countStudentHavingCSCourseBeforeMGCourse, countStudentHavingMGCourseBeforeCSCourse, examSchedule
    for student, coursesList in studentEnrolledCourses.items():
        checkCSCourseInFirstSlot = False
        checkMGCourseInFirstSlot = False
        for course in coursesList:
            i = 0
            for schedule in examSchedule:
                # print(schedule)
                for exam in schedule:
                    # print(exam)
                    if(i == 0):
                        if(course == exam[0]): # First check exams of the student in first slot
                            # print(course)
                            if("CS" in course):
                                # print(1)
                                checkCSCourseInFirstSlot = True
                            elif("MG" in course):
                                checkMGCourseInFirstSlot = True
                    else:
                        if(course == exam[0]): # Then check exams of the student in 2nd slot
                            print(checkCSCourseInFirstSlot)
                            print(checkMGCourseInFirstSlot)
                            if("CS" in course and checkMGCourseInFirstSlot):
                                countStudentHavingMGCourseBeforeCSCourse+=1
                            elif("MG" in course and checkCSCourseInFirstSlot):
                                countStudentHavingCSCourseBeforeMGCourse+=1
                            checkCSCourseInFirstSlot = False
                            checkMGCourseInFirstSlot = False
                if(i == 0):
                    i+=1
                else:
                    i=0
    print(countStudentHavingCSCourseBeforeMGCourse)
    print(countStudentHavingMGCourseBeforeCSCourse)

def priortizeCSCourseOverMGCourse():
    computeCSAndMGCourseAlignmentForADayRatio()
    # print(studentEnrolledCourses)
    return 1

# Compute the schedule
def computeSchedule():
    global examSchedule, countCourseRegisteredStudents
    importRandomTeachersForADay()
    remainingExamsList = convertDictionaryToList(countCourseRegisteredStudents)
    while(len(remainingExamsList) > 0):
        remainingExamsList = createCombination(remainingExamsList)
    # print(examSchedule)
    
initializeVariables()
computeSchedule()
priortizeCSCourseOverMGCourse()