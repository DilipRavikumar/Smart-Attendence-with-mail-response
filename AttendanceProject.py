import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText

# Add your email and SMTP configurations here
myEmail = 'projectzx619@gmail.com'
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_password = 'vbwb huma hkoe essp'

# Dictionary to map student names to email addresses
student_data = {
    "244019": "jaiprakash292033@gmail.com",
    "244022": "kabilkabilan02@gmail.com",
    "244010": "mailthistodilip@gmail.com",  # Mapping for student "244010"
    # Add more student email mappings here
}

path = 'Images_Attendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def send_email(subject, message, to_email):
    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = myEmail
        msg['To'] = to_email

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(myEmail, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email} successfully.")
    except Exception as e:
        print(f"An error occurred while sending the email to {to_email}: {str(e)}")

def get_student_email(student_name):
    # Check if the student name exists in the data source and return the email address.
    return student_data.get(student_name, None)

def markAttendance(name, email):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            f.write(f'\n{name},{tString},{dString}')
            send_email("Attendance Notification", f"You were marked present on {dString} at {tString}.", email)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            student_email = get_student_email(name)
            if student_email:
                markAttendance(name, student_email)
            else:
                print(f"Email address not found for {name}")
        else:
            # Delay for 3 seconds for incorrect recognition
            time.sleep(3)
    cv2.imshow('webcam', img)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindows()
