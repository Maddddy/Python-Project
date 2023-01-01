import mysql.connector
import csv
import json
import pandas
from matplotlib import pyplot

def enterMarks(course_id):
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
    cursorObject = mydb.cursor()
    cursorObject.execute("SELECT * FROM course")
    myresult = cursorObject.fetchall()
    course_name = ""
    csv_reader = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    marks = {}
    for i in range(0, len(myresult)):
        if(myresult[i][0] == course_id):
            course_name = myresult[i][1]
    course_name = ""
    student_marks = {}
    for i in range(1, len(csv_reader)):
        if(csv_reader[i][0] == course_id):
            check = 1
            course_name = csv_reader[i][1]
            student_marks = json.loads(csv_reader[i][2])
            break
    if(check == 0):
        return marks
    else:
        print("Course name: " + course_name)
        mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
        cursorObject1 = mydb1.cursor()
        cursorObject1.execute("SELECT * FROM batch")
        myresult1 = cursorObject1.fetchall()
        for i in range(0, len(myresult1)):
            courses = list(myresult1[i][3].split(":"))
            for j in range(0, len(courses)):
                if(courses[j] == course_id):
                    students = list(myresult1[i][4].split(":"))
                    for k in students:
                        marks_obtained = int(input("Enter marks obtained by " + k + ": "))
                        marks[k] = marks_obtained
    return marks
    print("Course ID does not exist")
    return
    student_ids = list(student_marks.keys())
    print("Course name: " + course_name)
    for student in student_ids:
        marks = int(input("Enter marks obtained by " + student + ": "))
        student_marks[student] = marks
    df = pandas.read_csv("course.csv")
    df.loc[i - 1, "marks_obtained"] = json.dumps(student_marks)
    df.to_csv("course.csv", index = False)

def viewPerformanceE(course_id):
    marks = enterMarks(course_id)
    if(len(marks) == 0):
        print("Course does not exist / No students enrolled in course")
    else:
        print("Marks obtained: ")
        for key, value in marks.items():
            print(key + ": ", value)
    csv_reader = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    check = 0
    student_marks = {}
    for i in range(0, len(csv_reader)):
        if(csv_reader[i][1] == course_id):
            check = 1
            student_marks = json.loads(csv_reader[i][2])
            break
    if(check == 0):
        print("Course ID does not exist")
        return
    student_ids = list(student_marks.keys())
    for student in student_ids:
        marks = student_marks[student]
        print("Marks obtained by " + str(marks))

def scatterPlot():
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "course")
    cursorObject = mydb.cursor()
    cursorObject.execute("SELECT * FROM course")
    myresult = cursorObject.fetchall()
    courses = []
    for i in range(0, len(myresult)):
        courses.append(myresult[i][0])
    mydb1 = mysql.connector.connect(host = "localhost", user = "root", password = "*******", database = "batch")
    cursorObject1 = mydb1.cursor()
    cursorObject1.execute("SELECT * FROM batch")
    myresult1 = cursorObject1.fetchall()
    csv_reader = []
    with open("course.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    all_marks = []
    for i in range(1, len(csv_reader)):
        all_marks.append(json.loads(csv_reader[i][2]))
    batches = []
    performance = []
    for i in range(0, len(myresult1)):
        batches.append(myresult1[i][0])
        performance.append(0)
    for i in range(0, len(courses)):
        marks = enterMarks(courses[i])
        keys = list(marks.keys())
        values = list(marks.values())
        for j in range(0, len(batches)):
            a = 0
            b = 0
            for k in range(0, len(keys)):
                x = keys[k]
                if(batches[j] == x[:5]):
                    a += values[k]
                    b += 1
            if(isinstance(b, int) and b != 0):
                performance[j] = a/b
        pyplot.scatter(batches, performance)
    students = []
    with open("batch.csv", "r", newline = "\n") as f:
        csv_reader = list(csv.reader(f, delimiter=","))
    for i in range(0, len(csv_reader)):
        batches.append(csv_reader[i][0])
        students.append(csv_reader[i][4].split(":"))
    for course in all_marks:
        batch_performances = []
        batchesX = []
        for i in range(0, len(batches)):
            total_marks = 0
            divs = 0
            check = 0
            for student in students[i]:
                if(student == students[i][0]):
                    if(not isinstance(course.get(student), int)):
                        check = 1
                        break
                total_marks += course.get(student)
                divs += 1
            if(check == 1):
                continue
            else:
                batchesX.append(batches[i])
                batch_performances.append(total_marks/divs)
        pyplot.scatter(batchesX, batch_performances)
    pyplot.show()
