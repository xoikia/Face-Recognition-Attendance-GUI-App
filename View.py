import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3


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

    # inserting values
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


def view_atlog():
    window = Tk()
    window.title("Attendance Logs")
    window.resizable(0, 0)
    window_height = 600
    window_width = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    window.config(background="lavender blush")

    window.wm_iconbitmap("ALOG.ico")
    window.configure()
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(1, weight=1)

    header = Label(window, text='Attendance Logs', width=41, height=2, fg="ghost white", bg="rosy brown",
                   anchor='center', relief=RAISED, font=("times", 18, 'bold'))
    header.place(x=0, y=2)

    tree = ttk.Treeview(window, height=24)
    tree['columns'] = ("UserId", "Name", "Department", "Date", "Time")

    tree.column("#0", width=0, stretch=NO)
    tree.column("UserId", anchor=CENTER, width=80)
    tree.column("Name", anchor=CENTER, width=160)
    tree.column("Department", anchor=CENTER, width=120)
    tree.column("Date", anchor=CENTER, width=120)
    tree.column("Time", anchor=CENTER, width=120)

    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("UserId", text="User Id", anchor=CENTER)
    tree.heading("Name", text="Name", anchor=CENTER)
    tree.heading("Department", text="Department", anchor=CENTER)
    tree.heading("Date", text="Date", anchor=CENTER)
    tree.heading("Time", text="Time", anchor=CENTER)

    # inserting values
    conn = sqlite3.connect("AttendanceDB.db")
    cur = conn.cursor()
    list_datas = cur.execute("SELECT * FROM Daily_Attendance").fetchall()
    for i, data in enumerate(list_datas):
        tree.insert(parent='', index='end', iid=i, text="", values=data)

    tree.place(x=0, y=80)

    scrollbar = ttk.Scrollbar(window, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    window.mainloop()