from flask import Flask,render_template,Response,url_for,redirect
import cv2
from mySQL import *
import cv2 as cv

import pickle
import face_recognition
import numpy as np
import cvzone 
from db import rollNumGet
import datetime
now = datetime.datetime.now()
# cur_time = now.strftime("%H:%M")
import time

from pyzbar.pyzbar import decode


app=Flask(__name__)
# cur_time = now.strftime("%H:%M")
cur_time="08:35"

print("Encoded File Loading...")
file=open("EncodeFile.p","rb")
model=pickle.load(file)
file.close()
print("Encoded File Loaded")
knownEncodeList,studentIDs = model

mycursor.execute("SELECT id FROM student")
id_list = mycursor.fetchall()
qrcode_list=[]
for i in id_list:
    print(i[0])
    qrcode_list.append(str(i[0]))

sql="SELECT * FROM slot"
mycursor.execute(sql)
mySlot_time = mycursor.fetchall()
lec_start_time=[]
lec_off_time=[]
for time in mySlot_time:
    lec_start_time.append(time[2].split('-')[0])  
    lec_off_time.append(time[2].split('-')[1])
if cur_time >=lec_start_time[0] and cur_time <lec_off_time[0] :
    path_slotNum=1
elif cur_time >=lec_start_time[1] and cur_time <lec_off_time[1]:
    path_slotNum=2
elif cur_time >=lec_start_time[2] and cur_time <lec_off_time[2]:
    path_slotNum=3
elif cur_time >=lec_start_time[3] and cur_time <lec_off_time[3]:
    path_slotNum=4
elif cur_time >=lec_start_time[4] and cur_time <lec_off_time[4]:
    path_slotNum=5
elif cur_time >=lec_start_time[5] and cur_time <lec_off_time[5]:
    path_slotNum=6
marked_sheet=[]
path='DummyAttendance/slot_'+str(path_slotNum)+'.csv'
with open(path,"r+",newline="\n") as f:
    AttenList=f.readlines()
    # rec_list=[]
    for line in AttenList:
        entry=line.split(",")
        marked_sheet.append(entry[0])
                





    
def generate_frames():
    camera=cv2.VideoCapture(0)

    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            #face recognition----
            imgS=cv.resize(frame,(0,0),None,0.25,0.25)
            imgS=cv.cvtColor(imgS,cv.COLOR_BGR2RGB)
            # -----------------QR CODE--------------

            for qrcode in decode(frame):
                qrcode.data
                myData=qrcode.data.decode('utf-8')
                # print(myData)
                # myData= myData.split('+')
                # print(myData[1])
                if myData in qrcode_list:
                    # qrTxt='Registerd'
                    qrColor=(0,255,0)
                    
                    mycursor.execute("SELECT roll_no FROM student WHERE id="+myData)
                    r_no = mycursor.fetchone()
                    r_no = "+".join(r_no)
                    qrTxt=r_no

                    if myData in marked_sheet:
                        qrTxt ="Attendance Marked "+r_no
                        qrColor=(0,0,255)

                    else:
                        rollNumGet(myData,cur_time)


                else:
                    qrTxt='*Not Found'
                    qrColor=(0,0,255)
                pts=np.array([qrcode.polygon],np.int32)
                pts=pts.reshape((-1,1,2))
                cv.polylines(frame,[pts],True,qrColor,5)

                pts2 =qrcode.rect
                cv.putText(frame,qrTxt,(pts2[0],pts2[1]-10),cv.FONT_HERSHEY_SIMPLEX,color=(255,0,255),fontScale=0.5,thickness=1)


            # ---------End--------QR CODE--------------


            faceCurLoc=face_recognition.face_locations(imgS)
            encodeCurFrame=face_recognition.face_encodings(imgS,faceCurLoc)


            for encodeFace, faceLoc in zip(encodeCurFrame,faceCurLoc):
                matches=face_recognition.compare_faces(knownEncodeList,encodeFace)
                faceDis=face_recognition.face_distance(knownEncodeList,encodeFace)
                # print("matches",matches)
                # print("faceDis",faceDis)

                
                matchIndex=np.argmin(faceDis)
                print("FacDisList",faceDis)
                print("FacDis index ",faceDis[matchIndex])

                print("matchIndex",matchIndex)
                # print(type(faceDis))

                A, B = np.partition(faceDis, 1)[0:2]
                # print("1st = ",A)
                # print("2nd = ",B)
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox= x1,y1,x2-x1,y2-y1
                
                
                # if matches[matchIndex] and faceDis[matchIndex] < 0.40:
                if matches[matchIndex]:
                    # print(type(studentIDs[matchIndex]))
                    
                    boxColor=(0,255,0)

                    
                    mycursor.execute("SELECT roll_no FROM student WHERE id="+str(studentIDs[matchIndex]))
                    r_no = mycursor.fetchone()
                    r_no = "+".join(r_no)
                    faceTxt=r_no
                    if r_no in marked_sheet:
                        faceTxt ="Attendance Marked "+r_no
                        boxColor=(0,0,255)

                    else:
                        rollNumGet(studentIDs[matchIndex],cur_time)

                    
                    print("knownFace dis: ", faceDis[matchIndex])
                    cvzone.cornerRect(frame,bbox,rt=1,t=5,colorR=(220,218,168),colorC=boxColor)
                    cv.putText(frame,f'{faceTxt}',(50+x1,140+y1-10),cv.FONT_HERSHEY_SIMPLEX,color=boxColor,fontScale=1,thickness=1)

                else:
                # print("UnKnownFace")
                    cvzone.cornerRect(frame,bbox,rt=1,t=5,colorR=(70,57,230),colorC=(0,255,0))

                    cv.putText(frame,'unKnown',(50+x1,140+y1-10),cv.FONT_HERSHEY_SIMPLEX,color=(70,57,230),fontScale=1,thickness=1)
            
            #end of face rec....
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')





@app.route('/')
def index():
    camera.release()
    return render_template('list.html', attSheet=data)


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/start_webcam')
def new():
    print("new")
    camera=cv2.VideoCapture(0)

    cur_date=now.strftime('%d %b %Y')
    cur_day = now.strftime("%A")
    return render_template('webcam.html' ,date=cur_date, day= cur_day)
# @app.route('/train')
# def train():
#     file = open(r'EncodeData.py', 'r').read()
#     exec(file)
    
#     return redirect(url_for('index'))


@app.route('/train')
def train():
    return render_template('loading.html')

@app.route('/progress')
def progress():
    def generate():
        # Execute your long-running task here
        file = open(r'EncodeData.py', 'r').read()
        exec(file)
        
        # Generate progress updates
        for progress in range(0, 101, 10):
            yield f"data:{progress}\n\n"
            time.sleep(1)

        # Redirect to index page after completion
        yield "data:redirect\n\n"

    return Response(generate(), mimetype='text/event-stream')
    
if __name__=="__main__":
    app.run(debug=True)
