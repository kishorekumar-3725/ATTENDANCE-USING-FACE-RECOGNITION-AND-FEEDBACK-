import cv2
import numpy as np
import face_recognition
import os
import smtplib
from email.message import EmailMessage
#import details
from datetime import datetime
from datetime import date
# from PIL import ImageGrab
%store -r dic
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)
#print(dic)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
#print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown=findEncodings(images)
#print(len(encodeLiskKnown))
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M')
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            f.writelines(f'\n{name},{dtString},{d1}')
def email(name):
    for i in dic:
        if(i==name):
            emid=dic[i]
            #print(emid)
            break
    msg=EmailMessage()
    msg.set_content("Your Attendence have been marcked for today!")
    msg['subject']="Lendi Institute of Engineering and Technology!"
    msg['to']=emid
    
    user="latish9347@gmail.com"
    msg['from']=user
    password="umljhzlkolkaynrn"
    
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()

cap = cv2.VideoCapture(0)
name1="x"
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            if(name1==name):
                break
                #continue
            else:
                email(name)
                name1=name
            
cv2.imshow('Webcam',img)
cv2.waitKey(1)