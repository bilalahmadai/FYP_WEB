
from mySQL import *
import datetime
now = datetime.datetime.now()
# cur_time = now.strftime("%H:%M")
cur_date=now.strftime('%Y-%m-%d')
# cur_day = now.strftime("%A")

# cur_date='2023-05-07'
# cur_time = '08:31'
cur_day="Monday"
# print(cur_time)                    

sql="SELECT id FROM student"
mycursor.execute(sql)
student_all_ids=mycursor.fetchall()
print("student_all_ids",student_all_ids)


# path='DummyAttendance/slot_'+str(1)+'.csv'

# with open(path,"r+",newline="\n") as f:
#         AttenList=f.readlines()
#         # rec_list=[]
#         for line in AttenList:
#             entry=line.split(",")
#             rec_list.append(entry[0])
# print(rec_list)

# get student timetable
def FindAbsentStudent(slotNum,rollNum,cur_time):
    
    path='DummyAttendance/slot_'+str(slotNum)+'.csv'
    print(f"found Student {rollNum:-^50}")
    sql="SELECT * FROM student_timetable WHERE student_id=%s"
    val=(rollNum,)
    mycursor.execute(sql,val)
    student_timetable = mycursor.fetchall()
    # print("student_timetable   ",student_timetable)   # id, student_id, timetable_id  [(1, 1, 45)]
    # timeTable_FID=student_timetable[0][2]

    for slt_fid in student_timetable:
        # print("Timetable ID",slt_fid[2])
        timeTable_FID=slt_fid[2]
    # get timetable of specific student through tbl of student_timetable
        sql="SELECT * FROM time_table WHERE id=%s"
        val=(timeTable_FID,)
        mycursor.execute(sql,val)
        timetable = mycursor.fetchall()
        # print('timetable  ',timetable) #id,course_id,slot_id,day,teacher_id   [(45, 1, 1, 'Monday', 1)]
        course_fid=timetable[0][1]
        slot_fid=timetable[0][2]

        day_timetable=timetable[0][3]
        print('------day_timetable   ',day_timetable)

        teacher_fid=timetable[0][4]
        sql="SELECT * FROM course WHERE id=%s"
        val=(course_fid,)
        mycursor.execute(sql,val)
        CourseFID = mycursor.fetchone()

        sql="SELECT * FROM teacher WHERE id=%s"
        val=(teacher_fid,)
        mycursor.execute(sql,val)
        TeacherFID = mycursor.fetchone()

        

        # print(f"id,  student_id, {rollNum}  course_id,{CourseFID[0]}   teacher_id, {TeacherFID[0]}   date,  lec,   status")

    # id,  student_id,   course_id,   teacher_id,    date,  lec,   status



        sql="SELECT * FROM slot WHERE id=%s"
        val=(slot_fid,)
        mycursor.execute(sql,val)
        Slot_FID = mycursor.fetchone()
        slot_split=Slot_FID[2].split("-")
        print("time of slot_id  ",slot_split) #['08:30', '10:00am'] 08:30
        
        
        
        if cur_time > slot_split[0] and cur_time ==slot_split[1] and cur_day.lower()==day_timetable.lower():
            print(cur_time,"  yes Attendance Should mark here",slot_split[0],"-" ,slot_split[1])
            mycursor.execute("SELECT MAX(lec_num) FROM attendance_sheet WHERE student_id=%s AND course_id=%s AND teacher_id=%s", (rollNum,CourseFID[0],TeacherFID[0]))
            result = mycursor.fetchone()
            # print("type----------",type(result[0]))
            if result[0] is None:
            # If this is the first time the student is attending the lecture, set the lecture number to 1
                lecNum = 1
            else:
            # Otherwise, increment the lecture number
                lecNum = int(result[0]) + 1
            
            
            sql = "INSERT INTO attendance_sheet (student_id, course_id, teacher_id, date, lec_num, attendance_status) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (rollNum, CourseFID[0],TeacherFID[0],cur_date,lecNum,"A")
            mycursor.execute(sql, val)
            dbconn.commit()
            
              
            # mark_Attendance(path,rollNum,CourseFID[0],TeacherFID[0],cur_time)

        else:
            print("No Lecture at that time",slot_split[0],"-",slot_split[1])
            


sql="SELECT * FROM slot"
mycursor.execute(sql)
MySlot_time = mycursor.fetchall()
# lec_start_time=[]
lec_off_time=[]
for time in MySlot_time:
    # lec_start_time.append(time[2].split('-')[0])
    
    lec_off_time.append(time[2].split('-')[1])

print(lec_off_time)

# marked_list=[]
# not_marked=[]

for slot_path_no in range(1,7):
    marked_list=[]
    not_marked=[]
    off_time=lec_off_time[slot_path_no-1]
    print(f"starting file {slot_path_no:-^50}")
    path='DummyAttendance/slot_'+str(slot_path_no)+'.csv'
    with open(path,"r+",newline="\n") as f:
        AttenList=f.readlines()
        for line in AttenList:
            entry=line.split(",")
            marked_list.append(entry[0])
    print('marked_list  ',marked_list)
    print(f"off lecture {lec_off_time[slot_path_no-1]:=^20}")
    for s_id in student_all_ids:
        # print(s_id[0])
        if str(s_id[0]) not in marked_list:
            not_marked.append(str(s_id[0]))
            # print("not marked  ",str(s_id[0]))
            FindAbsentStudent(slot_path_no,str(s_id[0]),off_time)
        else:
            print("marked ",str(s_id[0]))
    print('not_marked  ',not_marked)
    
