# Face-Recognition-Attendance-GUI-App

A face recognition based attendance GUI which takes attendance and stores various data along with it.

The repository consists of 3 main files:
    
[app.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/Face_Scan.py). This is the main file which will run the GUI and also for cpaturing 
the image and storing its encodings.

[Face_scan.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/Face_Scan.py) This file is responsible for face recognition to take attendance

[View.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/View.py) This file helps to view the databases

Before explaining the code lets view the *flowchart* of the app.

<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/Flow%20chart.png" alt="IPL">
</p>


# Explanation of the files

First we will go through the codes of the **`Face_scan.py`** file.

This files is responsible for scanning the faces, detecting whether the faces are in the pickle file or not, if the face encodings are not present it will ask to register them 
first and if detected it takes attendance and stores the attendance logs and displaying it. All this process is done  by a single function **`scan_face`**. The function is bit  long so we will break into different parts for convenience

#### Part1
```    
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam = False
if os.path.isfile('./Face_Encodings.pkl'):
    cam = True

else:
    op = "Now Match Found, Please Register first!"
    tmsg.showinfo('Error', op)
```

This block of code is responsible for creating a varible which stores the video using cv2.VideoCapture. The if else block is repsonsible to check whether the Face_encodings.pkl
is present or not. Whenever a new user runs the program for the first time and directly try to scan his/her face it will give an error , so this else staements responsible to notify him that no encoding files is created till now and the cam variable doesn't changes it value and the while loops doesn't execute at all.

#### Part2
```python=
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
```
If the cam value is set to True, this while loops run. This block is responsbile for capturing the image and with the help of `face_recognition.face_locations` and `face_recognition.face_encodings` we are able to detect the locations of the face and then the encodings of the face at that location and store them into two varibel `face_loc` and `face_encode`. Now in the for loops all the recognition of faces are done. 

Now inside the for loop we first open the `Face_Encodings.pkl`(Details about this file will be explained in the `app.py`). This file stores the encodings of all the registered users faces and its corresponding userid's, we extract both these values into two variable `ke` and `knownnames`. After that we compare our `encode` file to the `ke` files(list) with the help of `face_recognition.compare_faces` and it returns a list with True or False , True if there is a match to any of the data in the list and False if no match. Then the `face_recognition.face_distance`  helps us to determine the value which has minimum difference  and store the index position which have  the minimum value to the `matchIndex` variable.
