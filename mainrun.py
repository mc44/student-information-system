# SIS made by Marc William M. Fajardo 2021
from tkinter import *
from tkinter import ttk, messagebox
import csv
import sqlite3
import courses
#from difflib import SequenceMatcher

window = Tk()
window.minsize(900, 600)
window.title("Student Information System")
window.resizable(False, False)
# constants
width = 900
height = 600
wrapper1 = LabelFrame(window, text="Edit")
pdown = 0.05
data_screenshot = []
# building tree view
tree_frame = Frame(window)
tree_frame.place(relx=0.01, rely=0.025+pdown, relheight=0.4, relwidth=0.98)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
my_tree['columns'] = ("ID", "Name", "Gender", "Year", "Course")
# #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=40)
my_tree.column("Name", anchor=W, width=160)
my_tree.column("Gender", anchor=CENTER, width=70)
my_tree.column("Year", anchor=CENTER, width=70)
my_tree.column("Course", anchor=CENTER, width=70)

# my_tree.heading("#0", text="#", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Name", text="Student Name", anchor=W)
my_tree.heading("Gender", text="Gender", anchor=CENTER)
my_tree.heading("Year", text="Year", anchor=CENTER)
my_tree.heading("Course", text="Course", anchor=CENTER)

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()

### Functions
#  load db and add data to treeview
def filltree(searchlimiter=""):
    my_tree.delete(*my_tree.get_children())
    conn = sqlite3.connect("sisdb.db")
    data = conn.execute("SELECT * FROM Students ").fetchall()
    conn.close()
    varlist = [var1.get(), var2.get(), var3.get(), var4.get(), var5.get()]
    iid = 1
    for line in data:
        if searchlimiter == "" or varlist == [0, 0, 0, 0, 0]:
            my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3], line[4]))
        else:
            c = 0
            text = ""
            for item in varlist:
                if item == 1:
                    text += str(line[c])
                c+=1
            if searchlimiter.lower() in text.lower():
                my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3], line[4]))
        iid += 1

def setlabel(labelvar, ddbox):
    counter = 0
    conn = sqlite3.connect("sisdb.db")
    course = conn.execute("SELECT * FROM Courses").fetchall()
    conn.close()
    for line in course:
        if ddbox.get() == line[0]:
            labelvar.config(text=f'{line[1]}')
            return

    #courselabel.config(text="{}".format())

def makecoursedropdown(ddbox):
    conn = sqlite3.connect("sisdb.db")
    course = conn.execute("SELECT * FROM Courses").fetchall()
    conn.close()
    Options = []
    for line in course:
        Options.append("{}".format(line[0]))
    ddbox['values'] = Options
    return course
    #print(Options[0].split(' - '))

def getcenterX(num):
    finnum = (window.winfo_screenwidth() / 2) - (num / 2)
    return finnum


def getcenterY(num):
    finnum = (window.winfo_screenheight() / 2) - (num / 2)
    return finnum

def getdatalist():
    data_list = []
    for line in my_tree.get_children():
        data = my_tree.item(line)['values']
        data_list.append(data)
        #data_list.append("{},{},{},{}".format(data[0], data[1], data[2], data[3]))
    return data_list

def updatedb(dlist):
    file = open("sisdb.csv", 'w', newline='')
    writer = csv.writer(file, delimiter=',')
    for line in dlist:
        writer.writerow(line)
    file.close()

def checkdb(sid, counter=-1):
    c = 0
    for val in data_screenshot:
        if str(val[0]) == str(sid) and counter != c:
            return TRUE
        c += 1
    return FALSE

def onFocus():
    tb_id.delete(0, END)
    tb_name.delete(0, END)
    tb_year.delete(0, END)
    tb_gender.delete(0, END)
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    tb_id.insert(0, values[0])
    tb_name.insert(0, values[1])
    tb_gender.insert(0, values[2])
    tb_year.insert(0, values[3])
    tb_course.set(values[4])
    setlabel(courselabel, tb_course)


def editOrDeleteEntry(delete=FALSE):
    global data_screenshot
    selected = my_tree.focus()
    if not selected:
        return
    #from treeview value
    values = my_tree.item(selected, 'values')
    sid = str(values[0])
    name = str(values[1])
    course = str(values[2])
    year = str(values[3])
    gender = str(values[4])
    #from onfocus
    s_tb = tb_id.get()
    n_tb = tb_name.get()
    c_tb = tb_course.get()
    y_tb = tb_year.get()
    g_tb = tb_gender.get()
    counter = 0

    if delete:
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            conn = sqlite3.connect("sisdb.db")
            data = conn.execute("DELETE FROM Students WHERE StudentID='{}'".format(sid))
            conn.commit()
            conn.close()
        else:
            return
    else:
        conn = sqlite3.connect("sisdb.db")
        data = conn.execute("SELECT * FROM Students WHERE StudentID='{}'".format(s_tb)).fetchall()
        if data!=[] and s_tb!=sid:
            messagebox.showinfo(parent=window, title="ID Exists", message="Inputted ID is already in the system")
            return
        elif not re.fullmatch(r"\d\d\d\d-\d\d\d\d", s_tb) and not delete:
            messagebox.showinfo(parent=window, title="ID Exists", message="Inputted ID is not in format ####-####")
            return
        edit = conn.execute(f'UPDATE Students SET StudentID=\'{s_tb}\', Name=\'{n_tb}\', Gender=\'{g_tb}\', YearLevel=\'{y_tb}\', CourseCode=\'{c_tb}\' WHERE StudentID=\'{sid}\'')
        conn.commit()
        conn.close()
    filltree()
    tb_id.delete(0, END)
    tb_name.delete(0, END)
    tb_course.set("")
    courselabel.config(text="")
    tb_year.delete(0, END)
    tb_gender.delete(0, END)
    tb_search.delete(0, END)
    return

def addEntry(button):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()

    def validate():
        t1 = tbox1.get()
        t2 = tbox2.get()
        t3 = tbox3.get()
        t4 = tbox4.get()
        t5 = tbox5.get()
        if t1 == "" or t2 == "" or t3 == "" or t4 == "" or t5 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        conn = sqlite3.connect("sisdb.db")
        data = conn.execute("SELECT * FROM Students WHERE StudentID='{}'".format(t1)).fetchall()
        if data != []:
            messagebox.showinfo(parent=addscreen, title="ID Exists", message="Inputted ID is already in the system")
            return
        elif not re.fullmatch(r"\d\d\d\d-\d\d\d\d", t1):
            messagebox.showinfo(parent=addscreen, title="ID Exists", message="Inputted ID is not in format ####-####")
            return
        add = conn.execute("INSERT INTO Students (StudentID, Name, Gender, YearLevel, CourseCode) VALUES ('{}','{}','{}','{}','{}')".format(t1, t2, t3, t4, t5))
        conn.commit()
        conn.close()
        filltree()
        button1.configure(state="normal")
        #global data_screenshot
        #data_screenshot = getdatalist()
        addscreen.destroy()

    addscreen = Toplevel(window)
    addscreen.resizable(False, False)
    addscreen.title("Add new Student")
    addscreen.geometry(f'{600}x{200}+{int(getcenterX(600))}+{int(getcenterY(200))}')
    addscreen.minsize(600, 200)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    label1 = ttk.Label(addscreen, text="ID")
    label2 = ttk.Label(addscreen, text="Name")
    label3 = ttk.Label(addscreen, text="Gender")
    label4 = ttk.Label(addscreen, text="Year")
    label5 = ttk.Label(addscreen, text="Course")
    tbox1 = ttk.Entry(addscreen, width=15)
    tbox2 = ttk.Entry(addscreen, width=15)
    tbox3 = ttk.Entry(addscreen, width=15)
    tbox4 = ttk.Entry(addscreen, width=15)
    clabel = ttk.Label(addscreen, text="")
    tbox5 = ttk.Combobox(addscreen)
    label1.place(relx=0.11, rely=0.045, relheight=0.1, relwidth=0.1)
    label2.place(relx=0.09, rely=0.195, relheight=0.1, relwidth=0.1)
    label3.place(relx=0.09, rely=0.345, relheight=0.1, relwidth=0.1)
    label4.place(relx=0.1, rely=0.495, relheight=0.1, relwidth=0.1)
    label5.place(relx=0.09, rely=0.645, relheight=0.1, relwidth=0.1)
    tbox1.place(relx=0.25, rely=0.045, relheight=0.11, relwidth=0.72)
    tbox2.place(relx=0.25, rely=0.195, relheight=0.11, relwidth=0.72)
    tbox3.place(relx=0.25, rely=0.345, relheight=0.11, relwidth=0.72)
    tbox4.place(relx=0.25, rely=0.495, relheight=0.11, relwidth=0.72)
    tbox5.config(state="readonly")
    courselist = makecoursedropdown(tbox5)
    tbox5.place(relx=0.25, rely=0.645, relheight=0.11, relwidth=0.42)
    clabel.place(relx=0.69, rely=0.645, relheight=0.09, relwidth=0.2)

    tbox5.bind('<<ComboboxSelected>>', lambda e: setlabel(clabel, tbox5))
    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.47, rely=0.83, relheight=0.12, relwidth=0.1)
# end addscreen

### end functions

filltree()
data_screenshot = getdatalist()
# set window on center screen
x = getcenterX(width)
y = getcenterY(height)
window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
onmodify = StringVar()
#main run

button1 = ttk.Button(window, text="Add Student", command=lambda: addEntry(button1))
button2 = ttk.Button(wrapper1, text="Edit Entry", command=lambda: editOrDeleteEntry())
button3 = ttk.Button(wrapper1, text="Delete Entry", command=lambda: editOrDeleteEntry(TRUE))
button4 = ttk.Button(window, text="Courses", command=lambda: courses.coursescreen(button4,tb_course))
lab_search = ttk.Label(window, text="Search:")
tb_search = ttk.Entry(window, textvariable=onmodify)
lab_id = ttk.Label(wrapper1, text="ID")
lab_name = ttk.Label(wrapper1, text="Name")
lab_course = ttk.Label(wrapper1, text="Course")
lab_year = ttk.Label(wrapper1, text="Year")
lab_gender = ttk.Label(wrapper1, text="Gender")
courselabel = ttk.Label(wrapper1, text="")
tb_id = ttk.Entry(wrapper1, width=15)
tb_name = ttk.Entry(wrapper1, width=15)
#options = StringVar(wrapper1)
tb_course = ttk.Combobox(wrapper1)
tb_year = ttk.Entry(wrapper1, width=15)
tb_gender = ttk.Entry(wrapper1, width=15)


ch1 = Checkbutton(window, text='ID', variable=var1, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
ch2 = Checkbutton(window, text='Name', variable=var2, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
ch3 = Checkbutton(window, text='Gender', variable=var3, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
ch4 = Checkbutton(window, text='Year', variable=var4, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))
ch5 = Checkbutton(window, text='Course', variable=var5, onvalue=1, offvalue=0, command=lambda: filltree(str(tb_search.get())))


# placing widgets
lab_search.place(relx=0.011, rely=0.015, relheight=0.06, relwidth=0.1)
tb_search.place(relx=0.06, rely=0.0305, relheight=0.03, relwidth=0.465)
ch1.place(relx=0.525, rely=0.0305, relheight=0.03, relwidth=0.05)
ch2.place(relx=0.58, rely=0.0305, relheight=0.03, relwidth=0.06)
ch3.place(relx=0.65, rely=0.0305, relheight=0.03, relwidth=0.06)
ch4.place(relx=0.72, rely=0.0305, relheight=0.03, relwidth=0.06)
ch5.place(relx=0.79, rely=0.0305, relheight=0.03, relwidth=0.06)
lab_id.place(relx=0.11, rely=0.025+pdown, relheight=0.06, relwidth=0.1)
lab_name.place(relx=0.095, rely=0.145+pdown, relheight=0.06, relwidth=0.1)
lab_gender.place(relx=0.09, rely=0.265+pdown, relheight=0.06, relwidth=0.1)
lab_year.place(relx=0.1, rely=0.385+pdown, relheight=0.06, relwidth=0.1)
lab_course.place(relx=0.09, rely=0.505+pdown, relheight=0.06, relwidth=0.1)
tb_id.place(relx=0.25, rely=0.025+pdown, relheight=0.08, relwidth=0.72)
tb_name.place(relx=0.25, rely=0.145+pdown, relheight=0.08, relwidth=0.72)
tb_gender.place(relx=0.25, rely=0.265+pdown, relheight=0.08, relwidth=0.72)
tb_year.place(relx=0.25, rely=0.385+pdown, relheight=0.08, relwidth=0.72)
tb_course.config(state="readonly")
courselist = makecoursedropdown(tb_course)
tb_course.place(relx=0.248, rely=0.505+pdown, relheight=0.09, relwidth=0.42)
courselabel.place(relx=0.69, rely=0.505+pdown, relheight=0.09, relwidth=0.2)


my_tree.pack(fill=BOTH)
tree_scroll.config(command=my_tree.yview)
button1.place(relx=0.01, rely=0.45+pdown, relheight=0.05, relwidth=0.2)
button2.place(relx=0.25, rely=0.65+pdown, relheight=0.11, relwidth=0.2)
button3.place(relx=0.47, rely=0.65+pdown, relheight=0.11, relwidth=0.2)
button4.place(relx=0.01, rely=0.51+pdown, relheight=0.05, relwidth=0.2)
wrapper1.place(relx=0.25, rely=0.43+pdown, relheight=0.45, relwidth=0.7)


#events
my_tree.bind('<<TreeviewSelect>>', lambda e: onFocus())
tb_course.bind('<<ComboboxSelected>>', lambda e: setlabel(courselabel, tb_course))
#tb_course.bind('<<OptionmenuSelect>>', lambda e: setlabel())
onmodify.trace("w", lambda name, index, mode, onmodify=onmodify: filltree(str(tb_search.get())))

window.mainloop()
