import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode

img=cv.imread('11.png')
qrcode_list=['11','14']
code=decode(img)
camera=cv.VideoCapture(0)

while True:
            
    print("hello")
        ## read the camera frame
    success,img=camera.read()
    for qrcode in decode(img):
        qrcode.data
        myData=qrcode.data.decode('utf-8')
        print(myData)
        # myData= myData.split('+')
        # print(myData[1])
        if myData in qrcode_list:
            qrTxt='Registerd'
            qrColor=(0,255,0)
        else:
            qrTxt='Not Found'
            qrColor=(0,0,255)
        pts=np.array([qrcode.polygon],np.int32)
        pts=pts.reshape((-1,1,2))
        cv.polylines(img,[pts],True,qrColor,5)

        pts2 =qrcode.rect
        cv.putText(img,myData+qrTxt,(pts2[0],pts2[1]-10),cv.FONT_HERSHEY_SIMPLEX,color=(255,0,255),fontScale=0.5,thickness=1)

    cv.imshow("result",img)
    cv.waitKey(1)
