from flask import Flask,render_template,Response,url_for
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    print("index")
    return render_template('list.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/start_webcam')
def new():
    print("new")
    curDate='10/04/2023'
    curDay='Monday'
    return render_template('webcam.html' ,date=curDate, day= curDay)
if __name__=="__main__":
    app.run(debug=True)
