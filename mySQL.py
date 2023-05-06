import mysql.connector
dbconn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="attendance_system"

)

mycursor = dbconn.cursor()
if (dbconn):
    print("DB successfull")
else:
    print("DB not successfull")
# SELECT asheet.id, student.name, student.roll_no, course.course_name, teacher.teacher_name, asheet.date, asheet.lec_num, asheet.attendance_status FROM attendance_sheet asheet
# INNER JOIN student ON asheet.student_id = student.id
# INNER JOIN course ON asheet.course_id = course.id
# INNER JOIN teacher ON asheet.teacher_id = teacher.id

mycursor.execute('''SELECT asheet.id, student.name, student.roll_no, course.name, teacher.name, asheet.date, asheet.lec_num, asheet.attendance_status FROM attendance_sheet asheet 
INNER JOIN student ON asheet.student_id = student.id
INNER JOIN course ON asheet.course_id = course.id
INNER JOIN teacher ON asheet.teacher_id = teacher.id
ORDER BY asheet.lec_num DESC''')
data = mycursor.fetchall()
print(data)