import pandas as pd
import numpy as np
import os
import csv
import random

courses, rooms, studentCourses, studentNames, teachers = [], [], [], [], []
countCourseRegisteredStudents = {}
studentsLimit  = 0
currentDate = [0,0] #Hour Shift , Day 
availableRooms = []
availableTeachers = []

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

def calculateStudentsLimitInRooms():
    global studentsLimit
    for i, roomNumber, capacity in rooms.itertuples():
        studentsLimit += int(capacity)

def returnCourseRegisteredStudentsAsList():
    return list(countCourseRegisteredStudents.items())

def randomlyPickExamAndReturnListOfExams(entry_list):
    exam = random.choice(entry_list)
    entry_list.remove(exam)
    return exam, entry_list

def resetDataForNextDay():
    return 1

def returnTimeAndDate():
    assignTimeStamp = 0
    assignDate = currentDate[1]
    if(currentDate[0] == 0):
        assignTimeStamp = 9
        currentDate[0] = 1
    else:
        assignTimeStamp = 2
        currentDate[0] = 0
        currentDate[1] += 1
        resetDataForNextDay()

    return assignTimeStamp, assignDate

def returnTeacher():
    return 1

def returnRoom():
    return 1

def assignRoomTeacherAndTime(result):
    time, date = returnTimeAndDate()
    return 1

def createCombination(exam, remainingExamsList):
    results = []
    totalSum = exam[1]
    results.append(exam)
    random.shuffle(remainingExamsList)
    for exam in remainingExamsList:
        if( (totalSum+exam[1]) <= studentsLimit):
            totalSum += exam[1]
            results.append(exam)
            remainingExamsList.remove(exam)

importFiles()
countStudentsInCourse()
calculateStudentsLimitInRooms()
exam, remainingExamsList = randomlyPickExamAndReturnListOfExams(returnCourseRegisteredStudentsAsList())
# print(exam)
# print(remainingExamsList)
# exam = ('JK123', 23)
# remainingExamsList = [('Pk', 30), ('LI', 50),  ('MNA', 20)]
createCombination(exam, remainingExamsList)