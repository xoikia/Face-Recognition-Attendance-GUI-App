import os
import cv2
import pickle
import sqlite3
import numpy as np
import datetime as dt
import face_recognition
import tkinter.messagebox as tmsg


def scan_face(label, var):
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam = False
    if os.path.isfile('./Face_Encodings.pkl'):
        cam = True

    else:
        op = "Now Match Found, Please Register first!"
        tmsg.showinfo('Error', op)


    while cam:
        ret, img = capture.read()
        image = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(image)
        face_encode = face_recognition.face_encodings(image, face_loc)

        for encode, loc in zip(face_encode, face_loc):
            with open("Face_Encodings.pkl", "rb") as ef:
                knownencodings = pickle.load(ef)
                ke = knownencodings[0]
                knownnames = pickle.load(ef)

            matches = face_recognition.compare_faces(ke, encode)
            faceDis = face_recognition.face_distance(ke, encode)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                getid = knownnames[matchIndex].upper()
                y1, x2, y2, x1 = loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, getid, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                conn1 = sqlite3.connect("Database.db")
                cur1 = conn1.cursor()

                name = cur1.execute("SELECT Name FROM Registered_User WHERE UserID =?", [getid]).fetchone()[0]
                dept = cur1.execute("SELECT Department FROM Registered_User WHERE UserID = ?", [getid]).fetchone()[0]
                conn1.close()

                conn2 = sqlite3.connect("AttendanceDB.db")
                cur2 = conn2.cursor()

                try:
                    cur2.execute("""CREATE TABLE Daily_Attendance (
                                         UserID TEXT NOT NULL,
                                         Name TEXT NOT NULL,
                                         Department TEXT NOT NULL,
                                         Date TEXT NOT NULL,
                                         Time TEXT NOT NULL
                                         )""")

                    conn2.commit()
                except sqlite3.OperationalError:
                    None

                conn2.close()

                date = dt.date.today().strftime("%b-%d-%Y")
                time = dt.datetime.now().strftime("%H:%M:%S")
                conn2 = sqlite3.connect("AttendanceDB.db")
                cur2 = conn2.cursor()

                cur2.execute(
                    "INSERT INTO Daily_Attendance VALUES (:id, :name, :department, :Date, :Time)",
                    {'id': getid, 'name': name, 'department': dept,
                     'Date': date,
                     'Time': time
                     })
                conn2.commit()
                conn2.close()

                cv2.imshow('Image', img)
                label.update()
                var.set("Welcome " + name+". Your login time is : " +time)

            else:
                print('No match')
                cv2.imshow('Image', img)
                op = "Now Match Found, Please Register first!"
                tmsg.showinfo('Error', op)

        cv2.waitKey(1000)
        break

    cv2.destroyAllWindows()