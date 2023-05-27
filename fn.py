# from db import rollNumGet
from mySQL import *
rollno='5'
cur_time='18:31'

import datetime
now = datetime.datetime.now()
# cur_time = now.strftime("%H:%M")

# rollNumGet(rollno,cur_time)

# mycursor.execute("SELECT roll_no FROM student WHERE id="+str(18))
# r_no = mycursor.fetchone()
# r_no = "+".join(r_no)
# print(r_no)
# ---------------------------------------------------
# mycursor.execute("SELECT id FROM student")
# id_list = mycursor.fetchall()
# qrcode_list=[]
# for i in id_list:
#     print(i[0])
#     qrcode_list.append(i[0])
# print(qrcode_list[0])

# if '5' in qrcode_list:
#     print("yes")
# ---------------------------------------------------

s=1
def slotPath(slot_no):
    s=slot_no
    path='DummyAttendance/slot_'+str(slot_no)+'.csv'
    return path
slot_path=slotPath()
print(slot_path)


