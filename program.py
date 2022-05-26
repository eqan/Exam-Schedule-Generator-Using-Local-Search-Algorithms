import pandas as pd
import numpy as np
import os
import csv

courses, rooms, studentCourses, studentNames, teachers = [], [], [], [], []
countCourseRegisteredStudents = {}

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

importFiles()
countStudentsInCourse()
print(countCourseRegisteredStudents)
