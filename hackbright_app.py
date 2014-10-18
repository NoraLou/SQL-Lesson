import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Project: %s 
    Description: %s
    Max Grade: %s""" %(row[0], row[1], row[2])

def get_grade_by_project(title):
    query = """SELECT Students.first_name, Projects.title, Grades.grade 
    FROM Students INNER JOIN Grades ON (Students.github= Grades.student_github) 
    INNER JOIN Projects ON (Grades.project_title = Projects.title) 
    WHERE title = ?"""
    DB.execute(query, (title,))
    projectrows = DB.fetchall()
    print title
    return projectrows



def get_grade_by_project_given_github(github):
    query = """SELECT Students.github, Projects.title, Grades.grade 
    FROM Students INNER JOIN Grades ON (Students.github= Grades.student_github) 
    INNER JOIN Projects ON (Grades.project_title = Projects.title) 
    WHERE github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    return rows

def get_grades_by_first_name(first_name):
    query = """SELECT Students.first_name, Projects.title, Grades.grade 
    FROM Students INNER JOIN Grades ON (Students.github= Grades.student_github) 
    INNER JOIN Projects ON (Grades.project_title = Projects.title) 
    WHERE Students.first_name = ?"""
    
    for row in DB.execute(query, (first_name,)):
        print """\
        First Name: %s 
        Project Title: %s
        Student Grade: %s""" %(row[0], row[1], row[2])
       


    # rows = DB.execute(query, (first_name,))
    # for row in rows:
    #     row = DB.fetchone()
    #     print """\
    #     First Name: %s 
    #     Project Title: %s
    #     Student Grade: %s""" %(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("""HBA Database > 
            Type student and github to do a lookup, 
            OR new_student and first, last, github to add a student,  
            OR title, followed by project title for project details,
            OR enter 'new_project' followed by: project title, description, and max_grade to create new project
            OR enter 'title_grade' to get student grades by project title  
            OR enter 'new_grade', github, project title, grade to enter a new grade for a student 
            OR enter 'get_grades' and enter first name of a student to view all their grades  """)
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "title":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "title_grade":
            get_grade_by_project(*args)
        elif command == "new_grade":
            make_new_grade (*args)
        elif command == "get_grades":
            get_grades_by_first_name(*args)

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s"%(first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects (title,description,max_grade) values (?, ?, ?)"""
    DB.execute(query,(title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s %s %s"%(title, description, max_grade)

def make_new_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s %s %s"%(student_github, project_title, grade)


    CONN.close()

if __name__ == "__main__":
    main()
