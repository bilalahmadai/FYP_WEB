from flask import Flask,render_template,Response,url_for,redirect
import cv2
from mySQL import *
import cv2 as cv

import pickle
import face_recognition
import numpy as np
import cvzone 
# from db import rollNumGet
import datetime
now = datetime.datetime.now()
# cur_time = now.strftime("%H:%M")
import time

from pyzbar.pyzbar import decode


app=Flask(__name__)
camera=cv2.VideoCapture(0)
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
                    # cur_time = now.strftime("%H:%M")
                    cur_time="10:35"
                    mycursor.execute("SELECT roll_no FROM student WHERE id="+myData)
                    r_no = mycursor.fetchone()
                    qrTxt = "+".join(r_no)
                    if myData in sheet_list:
                        qrTxt ="Attendance Marked"
                    else:
                    # rollNumGet(studentIDs[matchIndex],cur_time)
                        pass

                    




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
                    # cur_time = now.strftime("%H:%M")
                    cur_time="10:35"
                    mycursor.execute("SELECT roll_no FROM student WHERE id="+str(studentIDs[matchIndex]))
                    r_no = mycursor.fetchone()
                    r_no = "+".join(r_no)

                    # rollNumGet(studentIDs[matchIndex],cur_time)
                    print("knownFace dis: ", faceDis[matchIndex])
                    cvzone.cornerRect(frame,bbox,rt=1,t=5,colorR=(220,218,168),colorC=(0,255,0))
                    cv.putText(frame,f'{r_no}',(50+x1,140+y1-10),cv.FONT_HERSHEY_SIMPLEX,color=(0,255,0),fontScale=1,thickness=1)

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
