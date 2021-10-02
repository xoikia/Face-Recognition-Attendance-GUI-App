from tkinter import *
from View import *
from Face_Scan import *
import datetime as dt
import cv2
import pickle
import sqlite3
import tkinter as tk
import face_recognition


# capture images
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


# connection with the database
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


# storing values into database
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


mainmenu = Menu(window)
m1 = Menu(mainmenu, tearoff=0)
m1.add_command(label="Registered Database", command=view_rdb)
m1.add_command(label="Attendance Log", command=view_atlog)
mainmenu.add_cascade(label="View Database", menu=m1)
window.configure(menu=mainmenu)


header = Label(window, text='Attendance System',width=71, height=2 , fg="white", bg="SlateBlue3",anchor='center',
               font=("times", 18, 'bold'), relief=RAISED)
header.place(x=0, y=0)


regframe = Frame(window, width=450, height=450, bg="SlateBlue2", borderwidth=2, relief=GROOVE)
regframe.place(x=30, y=100)

loginframe = Frame(window, width=450, height=450, bg="SlateBlue2", borderwidth=2, relief=GROOVE)
loginframe.place(x=520, y=100)


# Registration part
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


# Attendance Frame
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

window.mainloop()

