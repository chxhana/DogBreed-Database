#!/usr/bin/env python3

'''A template for a simple app that interfaces with a database on the class server.
This program is complicated by the fact that the class database server is behind a firewall and we are not allowed to
connect directly to the MySQL server running on it. As a workaround, we set up an ssh tunnel (this is the purpose
of the DatabaseTunnel class) and then connect through that. In a more normal database application setting (in
particular if you are writing a database app that connects to a server running on the same computer) you would not
have to bother with the tunnel and could just connect directly.'''

import mysql.connector
import os.path
from db_tunnel import DatabaseTunnel

# Default connection information (can be overridden with command-line arguments)
# Change these as needed for your app. (You should create a token for your database and use its username
# and password here.)
DB_NAME = "cd0723_registration"
DB_USER = "token_7694"
DB_PASSWORD = "Pvi3yaNMOg7kqffX"

# SQL queries/statements that will be used in this program (replace these with the queries/statements needed
# by your program)
Search_Student = """
    SELECT Student.name
    FROM Student
    WHERE Student.id = %s
    ;
"""

Add_Student = """
    Insert into Student( id, name) VALUES(
    %s, %s )
    ;
"""

# Use "%s" as a placeholder for where you will need to insert values (e.g., user input)
Show_Course = """
    Select prefix, number, title
    From Course
    inner join  Enroll ON Course.prefix = Enroll.course_prefix and Course.number = Enroll.course_number
    inner join Student on Student.id = Enroll.student_id
    Where Student.id = %s
    ;
"""

Total_Credits = """
 select sum(Course.minCredits) as TotalCredits
 from Course
 inner join  Enroll ON Course.prefix = Enroll.course_prefix and Course.number = Enroll.course_number
 inner join Student on Student.id = Enroll.student_id
 where Student.id = %s
 ;
    
"""

Search_Class = """
 select prefix,number,title
 from Course
 where title like concat("%",%s,"%")
     ;
"""

Add_Class = """
    Insert into Enroll( student_id, course_prefix, course_number) VALUES(
    %s, %s, %s )
    ;
"""

Drop_Class = """
   Delete from Enroll
   Where student_id = %s and course_prefix = %s and course_number = %s 
    ;
"""


# If you change the name of this class (and you should) you also need to change it in main() near the bottom
class to_do:
    '''A simple Python application that interfaces with a database.'''

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
        self.dbHost, self.dbPort = dbHost, dbPort
        self.dbName = dbName
        self.dbUser, self.dbPassword = dbUser, dbPassword

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.dbHost, port=self.dbPort, database=self.dbName,
            user=self.dbUser, password=self.dbPassword,
            use_pure=True,
            autocommit=True,
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def runApp(self):
        # The main loop of your program
        # Take user input here, then call methods that you write below to perform whatever
        # queries/tasks your program needs.
        Student_id = int(input("\nEnter your student id : "))
        name = self.searchForStudentById(Student_id)
        if not name:
            answer = input("Student ID not found, would you like to be added? (y/n): ").lower()
            if answer == 'y':
                new_student = input("\nEnter your name : ")

                Student_id = int(input("\nEnter a new 6 digit student id : "))


            else:
                return
            self.addNewStudent(Student_id, new_student)
            print(f"Welcome {new_student}!")


            #self.addNewStudent(Student_id, new_student)
            self.showStudentCourses(Student_id)

        else:
                print("Hi " + self.searchForStudentById(Student_id) + " these are the classes you've registered for:")
                self.showStudentCourses(Student_id)
                self.getTotalStudentCredits(Student_id)




        while True:

            answer = input("\nWhat do you want to do?\ns) search for course \na) add course\nd) drop course" 
                           " \nq) enter q to exit\nEnter: ")
            if answer == 'q':
                break
            if answer == 's':
                keyword = input("Enter a course to search for: ")
                self.searchForClassByKeyword(keyword)
            elif answer == 'a':
                prefix, number = input("Enter prefix and number to add:").split()
                self.addClass(Student_id, prefix, number)
                self.showStudentCourses(Student_id)
            elif answer == 'd':
                prefix, number = input("Enter prefix and number to remove:").split()
                self.dropClass(Student_id, prefix, number)
                self.showStudentCourses(Student_id)


    # Add one method here for each database operation your app will perform, then call them from runApp() above

    # An example of a method that runs a query
    def searchForStudentById(self, student_id):
        # Execute the query
        self.cursor.execute(Search_Student, (student_id,))

        # Iterate over each row of the results
        for (name) in self.cursor:
            # Formatted strings (f"...") let you insert variables into strings by putting them in { }
            return name[0]

    # An example of a method that inserts a new row
    def addNewStudent(self, student_id,name,):
        self.cursor.execute(Add_Student, (student_id,name))

    def showStudentCourses(self, student_id):
        self.cursor.execute(Show_Course, (student_id,))
        for (prefix, number, title) in self.cursor:
            print(f"{prefix} {number} {title}")

    def getTotalStudentCredits(self, student_id):
        self.cursor.execute(Total_Credits, (student_id,))

        for (total_credits) in self.cursor:
            print(f"{total_credits[0]}" + " credits total")

    def searchForClassByKeyword(self, keyword):
        self.cursor.execute(Search_Class, (keyword,))
        for (prefix, number, title) in self.cursor:
            print(f"{prefix} {number} {title}")

    def addClass(self, student_id, course_prefix, course_number):
        self.cursor.execute(Add_Class, (student_id, course_prefix.upper(), course_number,))

    def dropClass(self, student_id, course_prefix, course_number ):
        self.cursor.execute(Drop_Class, (student_id, course_prefix, course_number,))




def main():
    import sys
    '''Entry point of the application. Uses command-line parameters to override database connection settings, then invokes runApp().'''
    # Default connection parameters (can be overridden on command line)
    params = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD
    }

    needToPrintHelp = False

    # Parse command-line arguments, overriding values in params
    i = 1
    while i < len(sys.argv) and not needToPrintHelp:
        arg = sys.argv[i]
        isLast = (i + 1 == len(sys.argv))

        if arg in ("-h", "-help"):
            needToPrintHelp = True
            break

        elif arg in ("-dbname", "-user", "-password"):
            if isLast:
                needToPrintHelp = True
            else:
                params[arg[1:]] = sys.argv[i + 1]
                i += 1

        else:
            print("Unrecognized option: " + arg, file=sys.stderr)
            needToPrintHelp = True

        i += 1

    # If help was requested, print it and exit
    if needToPrintHelp:
        printHelp()
        return

    try:
        with \
                DatabaseTunnel() as tunnel, \
                to_do(
                    dbHost='localhost', dbPort=tunnel.getForwardedPort(),
                    dbName=params['dbname'],
                    dbUser=params['user'], dbPassword=params['password']
                ) as app:

            try:
                app.runApp()
            except mysql.connector.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)

    except mysql.connector.Error as err:
        print("Error communicating with the database (see full message below).", file=sys.stderr)
        print(err, file=sys.stderr)
        print("\nParameters used to connect to the database:", file=sys.stderr)
        print(f"\tDatabase name: {params['dbname']}\n\tUser: {params['user']}\n\tPassword: {params['password']}",
              file=sys.stderr)
        print("""
(Did you install mysql-connector-python and sshtunnel with pip3/pip?)
(Are the username and password correct?)""", file=sys.stderr)


def printHelp():
    print(f'''
Accepted command-line arguments:
    -help, -h          display this help text
    -dbname <text>     override name of database to connect to
                       (default: {DB_NAME})
    -user <text>       override database user
                       (default: {DB_USER})
    -password <text>   override database password
    ''')


if __name__ == "__main__":
    main()