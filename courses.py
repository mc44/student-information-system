from tkinter import *
from tkinter import ttk, messagebox
import csv
import sqlite3

def coursescreen(coursebutton, tb_course):
    window = Tk()
    window.minsize(500, 400)
    window.title("Student Information System")
    window.resizable(False, False)
    window.after(1, lambda: window.focus_force())
    varcode = IntVar(window)
    varname = IntVar(window)

    def on_close():
        coursebutton.configure(state="normal")
        makecoursedropdown(tb_course)
        window.destroy()

    def makecoursedropdown(ddbox):
        conn = sqlite3.connect("sisdb.db")
        course = conn.execute("SELECT * FROM Courses").fetchall()
        conn.close()
        Options = []
        for line in course:
            Options.append("{}".format(line[0]))
        ddbox['values'] = Options
        return course
        # print(Options[0].split(' - '))

    def getcenterX(num):
        finnum = (window.winfo_screenwidth() / 2) - (num / 2)
        return finnum

    def getcenterY(num):
        finnum = (window.winfo_screenheight() / 2) - (num / 2)
        return finnum

    def filltree(searchlimiter=""):
        course_tree.delete(*course_tree.get_children())
        conn = sqlite3.connect("sisdb.db")
        data = conn.execute("SELECT * FROM Courses ").fetchall()
        conn.close()
        varlist = [varcode.get(), varname.get()]
        iid = 1
        for line in data:
            if searchlimiter == "" or varlist == [0, 0]:
                course_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1]))
            else:
                c = 0
                text = ""
                for item in varlist:
                    if item == 1:
                        text += str(line[c])
                    c += 1
                if searchlimiter in text:
                    course_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1]))
            iid += 1

    def onFocus():
        tb_id.delete(0, END)
        tb_name.delete(0, END)
        selected = course_tree.focus()
        values = course_tree.item(selected, 'values')

        tb_id.insert(0, values[0])
        tb_name.insert(0, values[1])

    def addEntry(button):
        def on_close():
            button.configure(state="normal")

            addscreen.destroy()

        def validate():
            t1 = tbox1.get()
            t2 = tbox2.get()
            if t1 == "" or t2 == "":
                messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
                return
            conn = sqlite3.connect("sisdb.db")
            data = conn.execute("SELECT * FROM Courses WHERE CourseCode='{}'".format(t1)).fetchall()
            if data != []:
                messagebox.showinfo(parent=addscreen, title="Course Code Exists", message="Inputted Course Coude is already in the system")
                return

            add = conn.execute("INSERT INTO Courses (CourseCode, Course) VALUES ('{}','{}')".format(t1, t2))
            conn.commit()
            conn.close()
            filltree()
            button.configure(state="normal")
            # global data_screenshot
            # data_screenshot = getdatalist()
            addscreen.destroy()

        addscreen = Toplevel(window)
        addscreen.resizable(False, False)
        addscreen.title("Add new Student")
        addscreen.geometry(f'{400}x{200}+{int(getcenterX(400))}+{int(getcenterY(200))}')
        addscreen.minsize(400, 200)
        button.configure(state="disabled")
        addscreen.protocol("WM_DELETE_WINDOW", on_close)

        label1 = ttk.Label(addscreen, text="Course Code")
        label2 = ttk.Label(addscreen, text="Course Name")
        tbox1 = ttk.Entry(addscreen, width=15)
        tbox2 = ttk.Entry(addscreen, width=15)
        label1.place(relx=0.09, rely=0.045, relheight=0.1, relwidth=0.3)
        label2.place(relx=0.09, rely=0.195, relheight=0.1, relwidth=0.3)
        tbox1.place(relx=0.35, rely=0.045, relheight=0.11, relwidth=0.62)
        tbox2.place(relx=0.35, rely=0.195, relheight=0.11, relwidth=0.62)

        add = ttk.Button(addscreen, text="Add", command=lambda: validate())
        add.place(relx=0.47, rely=0.83, relheight=0.12, relwidth=0.1)
    # end addscreen

    def editOrDeleteEntry(delete=FALSE):
        selected = course_tree.focus()
        if not selected:
            return
        # from treeview value
        values = course_tree.item(selected, 'values')
        sid = str(values[0])
        name = str(values[1])
        # from onfocus
        s_tb = tb_id.get()
        n_tb = tb_name.get()
        counter = 0

        if delete:
            result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning', parent=window)
            if result == 'yes':
                conn = sqlite3.connect("sisdb.db")
                data = conn.execute("DELETE FROM Courses WHERE CourseCode='{}'".format(sid))
                conn.commit()
                conn.close()
            else:
                return
        else:
            conn = sqlite3.connect("sisdb.db")
            data = conn.execute("SELECT * FROM Courses WHERE CourseCode='{}'".format(s_tb)).fetchall()
            if data != [] and s_tb != sid:
                messagebox.showinfo(parent=window, title="ID Exists", message="Inputted ID is already in the system")
                return
            edit = conn.execute("UPDATE Courses SET CourseCode='{}', Course='{}' WHERE CourseCode='{}'".format(s_tb, n_tb, sid))
            conn.commit()
            conn.close()
        filltree()
        tb_id.delete(0, END)
        tb_name.delete(0, END)
        return


    wrapper1 = LabelFrame(window, text="Edit")
    pdown = 0.05
    width=500
    height=400
    coursebutton.configure(state="disabled")
    window.protocol("WM_DELETE_WINDOW", on_close)
    # building tree view
    tree_frame = Frame(window)
    tree_frame.place(relx=0.01, rely=0.025+pdown, relheight=0.4, relwidth=0.98)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    course_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    course_tree['columns'] = ("Course Code", "Course Name")
    # #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
    course_tree.column("#0", width=0, stretch=NO)
    course_tree.column("Course Code", anchor=CENTER, width=40)
    course_tree.column("Course Name", anchor=W, width=160)

    course_tree.heading("Course Code", text="Course Code", anchor=CENTER)
    course_tree.heading("Course Name", text="Course Name", anchor=W)
    x = getcenterX(width)
    y = getcenterY(height)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    filltree()
    onmodify1 = StringVar(window)
    course_tree.pack(fill=BOTH)
    tree_scroll.config(command=course_tree.yview)

    button0 = ttk.Button(window, text="Add Course", command=lambda: addEntry(button0))
    button1 = ttk.Button(wrapper1, text="Edit Entry", command=lambda: editOrDeleteEntry())
    button2 = ttk.Button(wrapper1, text="Delete Entry", command=lambda: editOrDeleteEntry(TRUE))
    lab_search = ttk.Label(window, text="Search:")
    tb_search1 = ttk.Entry(window, textvariable=onmodify1)
    lab_id = ttk.Label(wrapper1, text="ID")
    lab_name = ttk.Label(wrapper1, text="Name")
    tb_id = ttk.Entry(wrapper1, width=15)
    tb_name = ttk.Entry(wrapper1, width=15)
    ch1 = Checkbutton(window, text='Course Code', variable=varcode, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search1.get())))
    ch2 = Checkbutton(window, text='Course Name', variable=varname, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search1.get())))

    # placing widgets
    lab_search.place(relx=0.011, rely=0.015, relheight=0.06, relwidth=0.1)
    tb_search1.place(relx=0.1, rely=0.0175, relheight=0.05, relwidth=0.465)
    ch1.place(relx=0.575, rely=0.0305, relheight=0.03, relwidth=0.18)
    ch2.place(relx=0.78, rely=0.0305, relheight=0.03, relwidth=0.18)
    lab_id.place(relx=0.11, rely=0.025 + pdown, relheight=0.1, relwidth=0.1)
    lab_name.place(relx=0.09, rely=0.175 + pdown, relheight=0.1, relwidth=0.1)
    tb_id.place(relx=0.25, rely=0.025 + pdown, relheight=0.12, relwidth=0.72)
    tb_name.place(relx=0.25, rely=0.185 + pdown, relheight=0.12, relwidth=0.72)

    button0.place(relx=0.01, rely=0.45 + pdown, relheight=0.07, relwidth=0.21)
    button1.place(relx=0.25, rely=0.65 + pdown, relheight=0.15, relwidth=0.25)
    button2.place(relx=0.55, rely=0.65 + pdown, relheight=0.15, relwidth=0.25)
    wrapper1.place(relx=0.25, rely=0.43 + pdown, relheight=0.47, relwidth=0.7)

    course_tree.bind('<<TreeviewSelect>>', lambda e: onFocus())
    onmodify1.trace("w", lambda name, index, mode, onmodify1=onmodify1: filltree(str(tb_search1.get())))

    window.mainloop()