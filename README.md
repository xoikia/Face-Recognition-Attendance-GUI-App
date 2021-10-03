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

### **`Face_scan.py`**

This files is responsible for scanning the faces, detecting whether the faces are in the pickle file or not, if the face encodings are not present it will ask to register them 
first and if detected it takes attendance and stores the attendance logs and displaying it. All this process is done  by a single function **`scan_face`**. The function is bit  long so we will break into different parts for convenience

#### Part1
```    
def scan_face(label, var):
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam = False
    if os.path.isfile('./Face_Encodings.pkl'):
        cam = True

    else:
        op = "Now Match Found, Please Register first!"
        tmsg.showinfo('Error', op)
```
The function takes two parameter, label is the label widget to which the function will be bind and the var will be explain at the last part of the code. This block of code is responsible for creating a varible which stores the video using cv2.VideoCapture. The if else block is repsonsible to check whether the `Face_encodings.pkl` is present or not. Whenever a new user runs the program for the first time and directly try to scan his/her face it will give an error , so this else staements responsible to notify him that no encoding files is created till now and the cam variable doesn't changes it value and the while loops doesn't execute at all.

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

In the `if` condition it checks whether the matches has a True or False in the `matchIndex` position, if it is **True** we extract the location and draw a rectangle over the user's face and display its UserID.

#### Part3
```
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
```
Here we are tyring to connect to the `Database` from which we are accesing the name and dept of the user which match the id we got earlier through the two `SQl select query`.
After that we create or open `AttendanceDB`. This Database will store the attendance logs of the users. We have used a `try` block inside which a `SQL Daily_Attendance` table is created if there is no such table, if the table exist the `try` blocks doesn't executes and the `except` block is run who does nothing and pass

#### Part4
```
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
```
This blocks maintains the attendance logs of the user by inserting into the `Daily_Attendance` table of `AttendanceDB`. First we store the current date and time into date and time varibales. Then we insert the `id, name, department, Date, Time` into the table and finally update the `var` variable with the welcome message. We will get to know  where this `var` variable will be used in the `app` file.

#### Part5
```
            else:
                cv2.imshow('Image', img)
                op = "Now Match Found, Please Register first!"
                tmsg.showinfo('Error', op)

        cv2.waitKey(1000)
        break

    cv2.destroyAllWindows()
```
If the `if` block inside  `PArt2` is `False` then `Part3, PArt4` doesn't executes at all and the `else` block is run. It creates info msg with `tmsg.showinfo` which tells the user that `Now Match Found, Please Register first!` and finally comes out of the loop wait for 1000ms and finally breaks out of the while loop and destroy the `cv2` window.
All the `Parts` were inside the `scan_face` function.


### **`View.py`**

This  file is responsible for creating two new windows which will help us to visualize our two databases. It contains two functions `view_rdb` and `view_atlog`. We will go through the two functions one by one.

#### **`view_rdb`**

The code will divided into parts for better understanding

#### Part1
```
def view_rdb():
    window = Tk()
    window.title("Registration Database")
    window.resizable(0, 0)
    window_height = 600
    window_width = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))


    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    window.config(background="azure")

    window.wm_iconbitmap("RDB.ico")
    window.configure()
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(1, weight=1)
```
This block of code is responsible for creating the `Registration Database` which will display the `Database` as a table. The window is created by creating a object `window` of `Tk` class of `Tkinter`. We set the title name to *Registration Database* and the `window.resizable(0, 0)` code prevents any user to resize the window from its default `600x600` width and height. The  `x_cordinate = int((screen_width / 2) - (window_width / 2))` and `y_cordinate = int((screen_height / 2) - (window_height / 2))` locates the screen at a fix position everytime the window is open. Before positioning any widgets inside the window we need to configure the row and column. the `window.grid_rowconfigure(2, weight=1)` and  `window.grid_columnconfigure(1, weight=1)` does this for us . It takes two values index and weight. Each row and column in the grid is identified by an index. The weight determines how wide the column/row will occupy, which is relative to other columns/rows.

#### Part2
```
    header = Label(window, text='Registration Database', width=41, height=2, fg="ghost white", bg="indian red",
                   anchor='center', relief=RAISED, font=("times", 18, 'bold'))
    header.place(x=0, y=2)

    tree = ttk.Treeview(window, height=24)
    tree['columns'] = ("UserId", "Name", "Mobile No", "Department", "Registration Date")

    tree.column("#0", width=0, stretch=NO)
    tree.column("UserId", anchor=CENTER, width=80)
    tree.column("Name", anchor=CENTER, width=160)
    tree.column("Mobile No", anchor=CENTER, width=100)
    tree.column("Department", anchor=CENTER, width=120)
    tree.column("Registration Date", anchor=CENTER, width=120)

    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("UserId", text="User Id", anchor=CENTER)
    tree.heading("Name", text="Name", anchor=CENTER)
    tree.heading("Mobile No", text="Mobile No", anchor=CENTER)
    tree.heading("Department", text="Department", anchor=CENTER)
    tree.heading("Registration Date", text="Registration Date", anchor=CENTER)
```
First we create a `header` variable which stores the label **Registration Database** using the `Label` method and place it  at the given coordinatess in the window. Then we create a `tree ` widget using `ttk.Treeview(window, height=24)`. Here, window refers to the main Tkinter application master node. We will have 5 columns `UserId, Name, MobileN No, Department, Registration Date` inside the table. We then formate our columns. Basically these allows us the assign `width` size  of the columns and how the data will be placed using anchor, `Anchors` are used to define where text is positioned relative to a reference point. Finally we create headings of the columns, the `text` refers to the label of the column and `anchor` is the relative position where it will be placed. Here it will be placed at the `center`. So our tree is built, now we will insert values in the tree from our database which we will explain in part3.

#### Part3
```
    conn = sqlite3.connect("Database.db")
    cur = conn.cursor()
    list_datas = cur.execute("SELECT * FROM Registered_User").fetchall()
    for i ,data in enumerate(list_datas):
        tree.insert(parent='', index='end', iid=i, text="", values=data)

    tree.place(x=0,y=80)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    window.mainloop()
```
We are connecting to our `Database`  and fetching all the values from it and storing in a variable `list_datas`. Here the values will be in the form of a list and each row in the database corresponds to a value in a list, meaning value in the index position 0 of the list stores all the values of row 1 of the database. We then iterate over the `list_datas` using a for loop and inserting every single values from the list into the tree with the `tree.insert(parent='', index='end', iid=i, text="", values=data)` code. Finally we place the table at a fixed coordinates using `tree.place(x=0, y=80)`. Then we create a `Scrollbar` widget and bind it to our main window and place at the `RIGHT` side of the window and the height is of same as the window height. We finally tell the Tkinter to run the window using `window.mainloop()`.


#### **`view_atlog`**
This function is mostly same as the `view_rdb`. The only changes are the `Label`, the label is `Attendance Logs`, names of the columns `UserId, Name, Department, Date, Time`
and the values that will be inserted. Here we will use the `AttendanceDB` and display it. Rest all the other code is same.
