# Face-Recognition-Attendance-GUI-App
<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/image.jpg" alt="img">
</p>


A face recognition based attendance GUI which takes attendance and stores various data along with it. The main libraries used are [tkinter](https://pypi.org/project/tkinter-page/), [face-recognition](https://pypi.org/project/face-recognition/), [open-cv](https://pypi.org/project/opencv-python/), [pickle](https://pypi.org/project/pickle5/)

The repository consists of 3 main files:
    
[app.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/Face_Scan.py). This is the main file which will run the GUI and also for cpaturing 
the image and storing its encodings.

[Face_scan.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/Face_Scan.py) This file is responsible for face recognition to take attendance

[View.py](https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/View.py) This file helps to view the databases

Before explaining the code lets view the *flowchart* of the app.

<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/Flow%20chart.png" alt="Flow chart">
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

### **`App.py`**
This is the main file which will run the main GUI window. Beside that it contains two functions `capture_image` and `store_delete`.
##### Part1 **`capture_image`**
This function will be bind to the `take_capture` button in the `Registration` frame, so whenever the button is clicked it will open the camera window and lets the user to capture its face and store its encodings.
```
def capture_image():
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = vid.read()
        text = "Press C to capture face"
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (55, 19, 0)
        frame = cv2.rectangle(frame, (20, 20), (620, 50), (235, 218, 164), -1)
        frame = cv2.putText(frame, text, (25, 40), font, 0.8, color, 2, cv2.LINE_AA)

        cv2.imshow('frame', frame)
        if cv2.waitKey(33) == ord('c'):
            print("Capturing image")
            image = cv2.resize(frame, (0, 0), None, fx=0.25, fy=0.25)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_loc = face_recognition.face_locations(image)
            face_encode = face_recognition.face_encodings(image, face_loc)
            try:
                with open("Face_Encodings.pkl", "rb") as f:
                    knownencodelist = pickle.load(f)
                    idlist = pickle.load(f)
                    print(knownencodelist)
                    print("appending")
                    knownencodelist[0].append(face_encode[0])
                    print(knownencodelist)
                    print("append complete")
                    idlist.append(id_entry.get())

                    open_pickle = open("Face_Encodings.pkl", 'wb')
                    pickle.dump(knownencodelist, open_pickle)
                    pickle.dump(idlist, open_pickle)
                    open_pickle.close()

            except:
                face = open("Face_Encodings.pkl", "wb")
                pickle.dump([face_encode], face)
                pickle.dump([id_entry.get()], face)
                face.close()

            break

    vid.release()
    cv2.destroyAllWindows()

    statusbar.update()
    statsvar.set(name_entry.get()+" your face is added successfully")
 ```
 First we use cv2.VideoCapture() to get a video capture object for the camera, then  we start a infinte loop. We create a rectange using `cv2.rectangle` and inside the rectangle we place a text using `cv2.putText`. It displays the text `Press C to capture face`. So whenever the user pressed `c` in the keyboard the `if` block run.
 
 Inside the if loop it first preprocess the frame it capture. It resize the image and convert BGR to RGB format. We are using the [face-recognition](https://pypi.org/project/face-recognition/) library. This library is responsible for identifying the locations as well as extracting the encodings of the faces from  the identified locations. The `face_recognition.face_locations(image)` command identifies the location of the faces from the frame and then we pass this locations to the `face_recognition.face_encodings(image, face_loc)`. This returns an n-dimensional array of the face enocdings of the users.The array will be stored in a list and any new face-encodings will be append into the list. This list stores the face-encodings of the users which we will used in the recognition process later on. We will convert htis list into byte stream using `pickle`. Due to the use of this library we are not building any neural network models or training it, we are simply passing the frame and the rest is handle by the library. 
 
 After that we create `try` and `except` block. The try blocks checks whether the `Face_Encodings.pkl` is located in our directory or not. This file stores the encodings of the faces. If it is found in our directory we open it and load the encodings and the id's using `knownencodelist = pickle.load(f)` and `idlist = pickle.load(f)`. Now the *knownencodelist* holds the previous encodings of the other user and now the encodings of the new user are appended to it and similarly the id's of the new user is appended to the *idlist*. The id is extracted from the tkinter `id_entry` widget with the help of `id_entry.get()` method. Now both the list contains the encodings and the id's of the new user along with the encodings and id's of the previous user. Pickle format doesn't allow us to update a existing file directly so we need to dump both the new lists inside the `Face_Encodings.pkl` which will overwrite the existing list, inorder to that we open the pickle file in `write` mode and dump the lists and finally close the file.
 
 If there is no `Face_Encodings.pkl` located in our directory the try block won't work and the `except` block run. It creates a `Face_Encodings.pkl` first then we dump both the encodings and the id's in the form of list and the close it, then finally we break out of the if loop as we had captured our image and stored our face-encodings along with our id's and close the camera window. After that it will update the `statusbar` widget of our GUI displaying that  *your face is added successfully*.
 
 #### Part2
 ```
conn = sqlite3.connect("Database.db")
cur = conn.cursor()
try:
    cur.execute("""CREATE TABLE Registered_User (
                         UserID TEXT NOT NULL,
                         Name TEXT NOT NULL,
                         MobileNo INTEGER NOT NULL,
                         Department TEXT NOT NULL,
                         Registered_Date TEXT)""")

    conn.commit()
except sqlite3.OperationalError:
    None

conn.close()
```
This code block creates/connects to a database named `Database` in our project folder. This database would store information of all the users who will register themselves. The `try` blocks creates a table `Registered_User` if the table doesn't exist. If the table exists the `except` block runs, it does nothing and fonally close the connection to our database. This table will store the information of the users. The value will be extratced from the respective `entry` widgets in the `Registration` frame.

#### Part3 **`store_delete`**
This function is responsible of extracting the values the user entered in the `entry` widget and storing it in the `Database` and finally clearing the entry widgets. This function will be bind to the `Save Profile` button in the `Registration` frame.
```
def store_delete():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()

    # inserting thr values into the database
    c.execute("INSERT INTO Registered_User VALUES (:id_entry, :name_entry, :phone_entry, :dep_entry, :Registered_Date)",
    {'id_entry': id_entry.get(), 'name_entry': name_entry.get(), 'phone_entry': phone_entry.get(),
     'dep_entry': dep_entry.get(), 'Registered_Date': dt.date.today().strftime("%b-%d-%Y")})

    conn.commit()
    conn.close()

    id_entry.delete(0, 'end')
    name_entry.delete(0, 'end')
    phone_entry.delete(0, 'end')
    dep_entry.delete(0, 'end')
    statusbar.update()
    statsvar.set('')
```
It first connects to the `Database` and then stores the value in the `Registered_User`table inside the database. The `.get()` method extracts values from all the entry widgets.
After inserting the values into the table we delete the values from the entry widget using the `.delete()` method and finally clears the statusbar widget too.

#### Part4 **`Building the main GUI`**
##### `1 Buidling the Window`
```
window = Tk()
window.title("Facial Attendance System")
window.resizable(0, 0)
window_height = 600
window_width = 1000
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
window.config(background="light blue")

window.wm_iconbitmap("logo.ico")
window.configure()
window.grid_rowconfigure(2, weight=1)
window.grid_columnconfigure(1, weight=1)
```
The above block of code builds the window of specified size and place it at the specified co-ordinates. It assigns a titel `Facial Attendance System` to the window. The 
`window.wm_iconbitmap("logo.ico")` lets us add a custom icon to our GUI and then we finally we configure the rows and columns.

##### `2 Adding Menus`
```
mainmenu = Menu(window)
m1 = Menu(mainmenu, tearoff=0)
m1.add_command(label="Registered Database", command=view_rdb)
m1.add_command(label="Attendance Log", command=view_atlog)
mainmenu.add_cascade(label="View Database", menu=m1)
window.configure(menu=mainmenu)
```
We are creating a Menu widgets. First we create a top menu which stores the menu `View Database`. This line of code `mainmenu.add_cascade(label="View Database", menu=m1)` performs this. The inside this menu we are adding two submenus. The 3rd and 4th line of code add the submenus. The submenus are `Registered Database` and `Attendance Log`.
This two menus are bind with the command `view_rdb` and `view_atlog` respectively. This are two functions from our `View.py` file. So whenever a user clicks the View Database he will have two options and as the user clicks anyone the respective function starts executing and a window pops out showing the database.

##### `3 Building the label and the two frames`
```
header = Label(window, text='Attendance System',width=71, height=2 , fg="white", bg="SlateBlue3",anchor='center',
               font=("times", 18, 'bold'), relief=RAISED)
header.place(x=0, y=0)


regframe = Frame(window, width=450, height=450, bg="SlateBlue2", borderwidth=2, relief=GROOVE)
regframe.place(x=30, y=100)

loginframe = Frame(window, width=450, height=450, bg="SlateBlue2", borderwidth=2, relief=GROOVE)
loginframe.place(x=520, y=100)
```
First we create the label of the GUI app , Our GUI app will have two separate frames, One is the `Registration` frame and the other is the `Attendance` frame. The above chunk of code just builds the two separate frame inside our main window.

##### `4 Registration frame`
This frames holds the necessary widgets such as labels, entry widgets  and the buttons to let a new user to register by capturing his/her image and storing their informations into the database. There are 4 entry widgets `id_entry, name_entry, phone_entry, dep_entry` and two buttons `Take Picture, Submit` and a `Staustbar` The entry widgets lets the user to enter the information and the `Take Picture`button is  bind with `capture_image` function defined ealier, so whenever a user clicks  it opens the camera window to take picture once the pciture is captured the `statusbar` is update. The `Submit` button is bind  with `store_submit` function. Once clicked it stores the information into the database and finally clears all the entry widgets and the statusbar. All this process of building and storing informations is done by below chunk of code.
```
reg_label=Label(regframe, text="Register New Employee", width=31, height=2, fg="white", bg="SlateBlue3",
                anchor="center", relief="raised", font=("times", 18, 'bold'))
reg_label.place(x=2,y=0)

id_label = Label(regframe, text="User ID", width=8, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                 relief="ridge")
id_label.place(x=10,y =60)
idvar = tk.StringVar()
id_entry = Entry(regframe, width=30, textvar=idvar, bg="white", fg="black",font=("times", 15, "bold"))
id_entry.place(x=100, y=65)

name_label = Label(regframe, text="Name", width=8, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                   relief="ridge")
name_label.place(x=10,y=120)
namevar = tk.StringVar()
name_entry = Entry(regframe, width=30, textvar=namevar, bg="white", fg="black",font=("times", 15, "bold"))
name_entry.place(x=100, y=125)

phone_label = Label(regframe, text="Mobile No", width=8, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                    relief="ridge")
phone_label.place(x=10, y=180)
phonevar = tk.IntVar()
phone_entry = Entry(regframe, width=30, textvar=phonevar, bg="white", fg="black",font=("times", 15, "bold"))
phone_entry.place(x=100, y=185)

dep_label = Label(regframe, text="Department", width=8, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                  relief="ridge")
dep_label.place(x=10,y=240)
depvar = tk.StringVar()
dep_entry = Entry(regframe, width=30, textvar=depvar, bg="white", fg="black",font=("times", 15, "bold"))
dep_entry.place(x=100, y=245)

pic_button = Button(regframe, text="Take Picture", command=capture_image, width=9, height=2, fg="white", bg="SlateBlue3",
                    font=("times", 12))
pic_button.place(x=110,y=300)

profile_button = Button(regframe, text="Save Profile", width=9, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                        command= store_delete)
profile_button.place(x=230, y=300)

status_label = Label(regframe, text="Status", width=8, height=2, fg="white", bg="SlateBlue3", font=("times", 12),
                     relief="ridge")
status_label.place(x=10, y=380)

statsvar = StringVar()
statusbar = Label(regframe, textvar=statsvar,  width=34, heigh=2, fg="white", bg="#FFA500", relief= RAISED,
                  font=("times", 13))
statusbar.place(x=90,y=380)
```
##### `5 Attendance Frame`
This frame holds the `label`, `Face Scan` button widget. The button widget is bind to the `scan_face` function of the `Face_Scan.py` file. This functios accepts two parameters. One is the `attstatus` label and the `attvar`. The first label will display a welcome message whenever the scan_face functions recognized the user for this the attvar is passed  which will be updated inside the function, by default it shows nothing but whenever a face is detected it is updated. When a user clicks on the `Face Scan` button the `scan_face` executes an window is opened which will match the face encodings with the list of encodings it has stored in the `Face_Encodings.pickle`.
```
att_label = Label(loginframe, text="Attendance", width=31, height=2, fg="white", bg="SlateBlue3", anchor="center",
                  relief="raised", font=("times", 18, "bold"))
att_label.place(x=2,y=0)

attvar = StringVar()
attstatus = Label(loginframe, textvar=attvar, width=60, height=23, fg="black", bg="gainsboro",
                  font=("times", 8, "bold"), relief=GROOVE)

face_button = Button(loginframe, text="Face Scan", command=(lambda: scan_face(attstatus, attvar)), width=30, height=1,
                     fg="white", bg="Green", anchor="center", font=("times", 18, "bold"), relief=GROOVE)
face_button.place(x=10, y=63)
attstatus.place(x=10, y=127)
```
Finally `window.mainloop()` this code runs the GUI app 

# OUTPUT

### **`MAIN GUI`**
<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/main%20gui.png" alt="MAIN GUI">
</p>

### **`Registration window`**
<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/register%20window.png" alt="REGS">
</p>

### **`AttendnaceLog window`**
<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/attendancelog%20window.png" alt="ATLOGS">
</p>

### **GUI IN ACTION**
<p align="center">
  <img src="https://github.com/xoikia/Face-Recognition-Attendance-Sysetm-GUI-App/blob/main/readme_images/Live%20GUI.gif" alt="Live GUI">
</p>
