# SIS made by Marc William M. Fajardo 2021
from tkinter import *
from tkinter import ttk, messagebox
import csv
from difflib import SequenceMatcher

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
my_tree['columns'] = ("ID", "Name", "Course", "Year")
# #0 column is the phantom column, parent-child relationship is not needed thus stretch=NO
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=40)
my_tree.column("Name", anchor=W, width=160)
my_tree.column("Course", anchor=CENTER, width=70)
my_tree.column("Year", anchor=CENTER, width=70)

# my_tree.heading("#0", text="#", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Name", text="Student Name", anchor=W)
my_tree.heading("Course", text="Course", anchor=CENTER)
my_tree.heading("Year", text="Year", anchor=CENTER)

### Functions
#  load db and add data to treeview
def filltree(searchlimiter=""):
    my_tree.delete(*my_tree.get_children())
    with open('sisdb.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        iid = 1
        for line in csv_reader:
            if searchlimiter == "":
                my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3]))
            else:
                #ratio = SequenceMatcher(None, searchlimiter, str(line[0])).ratio()
                #if len(str(line[0])) >= len(searchlimiter):
                #    score = float(len(searchlimiter)) / float(len(str(line[0])))
                    # if ratio>=score:
                if searchlimiter in str(line[0]):
                    my_tree.insert(parent='', index='end', iid=iid, text="", values=(line[0], line[1], line[2], line[3]))

            iid += 1

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
    tb_course.delete(0, END)
    tb_year.delete(0, END)
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    tb_id.insert(0, values[0])
    tb_name.insert(0, values[1])
    tb_course.insert(0, values[2])
    tb_year.insert(0, values[3])

def editOrDeleteEntry(delete=FALSE):
    global data_screenshot
    selected = my_tree.focus()
    if not selected:
        return
    values = my_tree.item(selected, 'values')
    sid = str(values[0])
    name = str(values[1])
    course = str(values[2])
    year = str(values[3])
    s_tb = tb_id.get()
    n_tb = tb_name.get()
    c_tb = tb_course.get()
    y_tb = tb_year.get()
    counter = 0
    for line in data_screenshot:
        if str(line[0]) == sid and str(line[1]) == name and str(line[2]) == course and str(line[3]) == year:
            break
        counter += 1
    c = data_screenshot[counter]
    if str(s_tb) == str(c[0]) and str(n_tb) == str(c[1]) and str(c_tb) == str(c[2]) and str(y_tb) == str(c[3]) and not delete:
        return
    if checkdb(s_tb, counter) and not delete:
        messagebox.showinfo(parent=window, title="ID Exists", message="Inputted ID is already in the system")
        return
    if delete:
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            data_screenshot.pop(counter)
        else:
            return
    else:
        data_screenshot[counter] = [tb_id.get(), tb_name.get(), tb_course.get(), tb_year.get()]
    updatedb(data_screenshot)
    filltree()
    tb_id.delete(0, END)
    tb_name.delete(0, END)
    tb_course.delete(0, END)
    tb_year.delete(0, END)
    tb_search.delete(0, END)

def addEntry(button):
    def on_close():
        button.configure(state="normal")
        addscreen.destroy()

    def validate():
        t1 = tbox1.get()
        t2 = tbox2.get()
        t3 = tbox3.get()
        t4 = tbox4.get()
        if t1 == "" or t2 == "" or t3 == "" or t4 == "":
            messagebox.showinfo(parent=addscreen, title="Incomplete Information", message="All textboxes need to be filled to complete the action")
            return
        if checkdb(t1):
            messagebox.showinfo(parent=addscreen, title="ID Exists", message="Inputted ID is already in the system")
            return
        my_tree.insert(parent='', index='end', iid=len(my_tree.get_children())+1, text="", values=(t1, t2, t3, t4))
        button1.configure(state="normal")
        updatedb(getdatalist())
        global data_screenshot
        data_screenshot = getdatalist()
        addscreen.destroy()

    addscreen = Toplevel(window)
    addscreen.resizable(False, False)
    addscreen.title("Add new Student")
    addscreen.geometry(f'{600}x{400}+{int(getcenterX(600))}+{int(getcenterY(400))}')
    addscreen.minsize(600, 400)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)

    label1 = ttk.Label(addscreen, text="ID")
    label2 = ttk.Label(addscreen, text="Name")
    label3 = ttk.Label(addscreen, text="Course")
    label4 = ttk.Label(addscreen, text="Year")
    tbox1 = ttk.Entry(addscreen, width=15)
    tbox2 = ttk.Entry(addscreen, width=15)
    tbox3 = ttk.Entry(addscreen, width=15)
    tbox4 = ttk.Entry(addscreen, width=15)
    label1.place(relx=0.11, rely=0.025, relheight=0.05, relwidth=0.1)
    label2.place(relx=0.09, rely=0.125, relheight=0.05, relwidth=0.1)
    label3.place(relx=0.09, rely=0.225, relheight=0.05, relwidth=0.1)
    label4.place(relx=0.1, rely=0.325, relheight=0.05, relwidth=0.1)
    tbox1.place(relx=0.25, rely=0.025, relheight=0.06, relwidth=0.72)
    tbox2.place(relx=0.25, rely=0.125, relheight=0.06, relwidth=0.72)
    tbox3.place(relx=0.25, rely=0.225, relheight=0.06, relwidth=0.72)
    tbox4.place(relx=0.25, rely=0.325, relheight=0.06, relwidth=0.72)

    add = ttk.Button(addscreen, text="Add", command=lambda: validate())
    add.place(relx=0.47, rely=0.7, relheight=0.06, relwidth=0.1)
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
lab_search = ttk.Label(window, text="Search:")
tb_search = ttk.Entry(window, textvariable=onmodify)
lab_id = ttk.Label(wrapper1, text="ID")
lab_name = ttk.Label(wrapper1, text="Name")
lab_course = ttk.Label(wrapper1, text="Course")
lab_year = ttk.Label(wrapper1, text="Year")
tb_id = ttk.Entry(wrapper1, width=15)
tb_name = ttk.Entry(wrapper1, width=15)
tb_course = ttk.Entry(wrapper1, width=15)
tb_year = ttk.Entry(wrapper1, width=15)

# placing widgets
lab_search.place(relx=0.011, rely=0.015, relheight=0.06, relwidth=0.1)
tb_search.place(relx=0.06, rely=0.0305, relheight=0.03, relwidth=0.465)
lab_id.place(relx=0.11, rely=0.025+pdown, relheight=0.06, relwidth=0.1)
lab_name.place(relx=0.09, rely=0.145+pdown, relheight=0.06, relwidth=0.1)
lab_course.place(relx=0.09, rely=0.265+pdown, relheight=0.06, relwidth=0.1)
lab_year.place(relx=0.1, rely=0.385+pdown, relheight=0.06, relwidth=0.1)
tb_id.place(relx=0.25, rely=0.025+pdown, relheight=0.08, relwidth=0.72)
tb_name.place(relx=0.25, rely=0.145+pdown, relheight=0.08, relwidth=0.72)
tb_course.place(relx=0.25, rely=0.265+pdown, relheight=0.08, relwidth=0.72)
tb_year.place(relx=0.25, rely=0.385+pdown, relheight=0.08, relwidth=0.72)

my_tree.pack(fill=BOTH)
tree_scroll.config(command=my_tree.yview)
button1.place(relx=0.01, rely=0.45+pdown, relheight=0.05, relwidth=0.2)
button2.place(relx=0.25, rely=0.55+pdown, relheight=0.11, relwidth=0.2)
button3.place(relx=0.47, rely=0.55+pdown, relheight=0.11, relwidth=0.2)
wrapper1.place(relx=0.25, rely=0.43+pdown, relheight=0.45, relwidth=0.7)

#events
my_tree.bind('<<TreeviewSelect>>', lambda e: onFocus())
onmodify.trace("w", lambda name, index, mode, onmodify=onmodify: filltree(str(tb_search.get())))

window.mainloop()
