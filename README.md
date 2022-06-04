# Exam-Schedule-Generator-Using-Local-Search-Algorithms
An exam schedule generator that generates a perfect solution for the exam using AI algorithms such as simuleated annealing based on cost factor and temperature.
We are generating an exam schedule that fullfills the constraints of two types

### Hard Constraints[Constraints that must be fulfilled] -> Perfect Solution
 - [x] An exam will be scheduled for each course.
 - [x] A student is enrolled in at least 3 courses. A student cannot give more than 1 exam at a time.
 - [x] Exam will not be held on weekends.
 - [x] Each exam must be held between 9 am and 5 pm
 - [x] Each exam must be invigilated by a teacher. A teacher cannot invigilate two exams at the same time.
 - [x] A teacher cannot invigilate two exams in a row.

### Soft Constraints[Constraints that we should try to fulfill to the max but not breaking the hard constraints] -> Best Solution
 - [x] All students and teachers shall be given a break on Friday from 1-2.
 - [x] A student shall not give more than 1 exam consecutively.
 - [x] If a student is enrolled in a MG course and a CS course, it is preferred that their MG course exam be held before their CS course exam.
 - [x] Two hours of break in the week such that at least half the faculty is free in one slot and the rest of the faculty is free in the other slot so the faculty meetings
shall be held in parts as they are now

You can read the research paper from which this project took inspiration: https://www.researchgate.net/publication/329997648_A_fast_simulated_annealing_algorithm_for_the_examination_timetabling_problem
