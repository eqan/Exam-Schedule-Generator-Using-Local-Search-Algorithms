import pandas as pd
import numpy as np
import os
import csv

courses, rooms, studentCourses, studentNames, teachers = [], [], [], [], []
countCourseRegisteredStudents = {}

def importFiles():
    global courses, rooms, studentCourses, studentNames, teachers
    courses = pd.read_csv(r'./courses.csv')
    rooms = pd.read_csv(r'./rooms.csv')
    studentCourses = pd.read_csv(r'./studentCourse.csv')
    studentNames = pd.read_csv(r'./studentNames.csv')
    teachers = pd.read_csv(r'./teachers.csv')

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

# print(courses)