from flask import Flask,render_template,Response,url_for,redirect
import cv2
from mySQL import *
import cv2 as cv

import pickle
import face_recognition
import numpy as np
import cvzone 
from db import rollNumGet



app=Flask(__name__)
camera=cv2.VideoCapture(0)
print("Encoded File Loading...")
file=open("EncodeFile.p","rb")
model=pickle.load(file)
file.close()
print("Encoded File Loaded")
knownEncodeList,studentIDs = model

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            #face recognition----
            imgS=cv.resize(frame,(0,0),None,0.25,0.25)
            imgS=cv.cvtColor(imgS,cv.COLOR_BGR2RGB)

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

                # print("matchIndex",matchIndex)
                # print(type(faceDis))

                A, B = np.partition(faceDis, 1)[0:2]
                # print("1st = ",A)
                # print("2nd = ",B)
                y1,x2,y2,x1=faceLoc
                y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                bbox= x1,y1,x2-x1,y2-y1
                
                
                if (matches[matchIndex]==True and A<B and A<=0.60):
                    # print(type(studentIDs[matchIndex]))
                    rollNumGet(studentIDs[matchIndex])
                    print("knownFace dis: ", faceDis[matchIndex])
                    cvzone.cornerRect(frame,bbox,rt=1,t=5,colorR=(220,218,168),colorC=(0,255,0))
                    cv.putText(frame,str(studentIDs[matchIndex]),(50+x1,140+y1-10),cv.FONT_HERSHEY_SIMPLEX,color=(0,255,0),fontScale=1,thickness=1)

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
    print("index")
    mycursor.execute('''SELECT asheet.id, student.name, student.roll_no, course.name, teacher.name, asheet.date, asheet.lec_num, asheet.attendance_status FROM attendance_sheet asheet
    INNER JOIN student ON asheet.student_id = student.id
    INNER JOIN course ON asheet.course_id = course.id
    INNER JOIN teacher ON asheet.teacher_id = teacher.id
    ORDER BY asheet.lec_num DESC''')
    data = mycursor.fetchall()
    # print(data)
    
    return render_template('list.html', attSheet=data)


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/start_webcam')
def new():
    print("new")
    curDate='10/04/2023'
    curDay='Monday'
    return render_template('webcam.html' ,date=curDate, day= curDay)
@app.route('/train')
def train():
    file = open(r'EncodeData.py', 'r').read()
    exec(file)
    
    return redirect(url_for('index'))
    
if __name__=="__main__":
    app.run(debug=True)
