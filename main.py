# SIS made by Marc William M. Fajardo 2021
from tkinter import *
from tkinter import ttk, messagebox
import csv


window = Tk()
window.minsize(900, 600)
window.title("Student Information System")
# constants
width = 900
height = 600
wrapper1= LabelFrame(window, text="Edit", padx=20, pady=10)

# building tree view
tree_frame = Frame(window)
tree_frame.place(relx=0.01, rely=0.025, relheight=0.4, relwidth=0.98)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)
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
def filltree():
    my_tree.delete(*my_tree.get_children())
    with open('sisdb.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        iid = 1
        for line in csv_reader:
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

def updatedb():
    data_list = getdatalist()
    with open("sisdb.csv", 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for line in data_list:
            writer.writerow(line)


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
        data_list = getdatalist()
        for val in data_list:
            if str(val[0]) == str(t1):
                messagebox.showinfo(parent=addscreen, title="ID Exists", message="Inputted ID is already in the system")
                return
        my_tree.insert(parent='', index='end', iid=len(my_tree.get_children())+1, text="", values=(t1, t2, t3, t4))
        button1.configure(state="normal")
        updatedb()
        addscreen.destroy()

    addscreen = Toplevel(window)
    addscreen.title("Add new Student")
    addscreen.geometry(f'{600}x{400}+{int(getcenterX(600))}+{int(getcenterY(400))}')
    addscreen.minsize(600, 400)
    button.configure(state="disabled")
    addscreen.protocol("WM_DELETE_WINDOW", on_close)
    name = ""
    id1 = ""
    course = ""
    year = ""
    label1 = ttk.Label(addscreen, text="ID")
    label2 = ttk.Label(addscreen, text="Name")
    label3 = ttk.Label(addscreen, text="Course")
    label4 = ttk.Label(addscreen, text="Year")
    tbox1 = ttk.Entry(addscreen, width=15, textvariable=id1)
    tbox2 = ttk.Entry(addscreen, width=15, textvariable=name)
    tbox3 = ttk.Entry(addscreen, width=15, textvariable=course)
    tbox4 = ttk.Entry(addscreen, width=15, textvariable=year)
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
# set window on center screen
x = getcenterX(width)
y = getcenterY(height)
window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

#main run
button1 = ttk.Button(window, text="Add Student", command=lambda: addEntry(button1))
# placing widgets
my_tree.pack(fill=BOTH)
tree_scroll.config(command=my_tree.yview)
button1.place(relx=0.01, rely=0.45, relheight=0.05, relwidth=0.2)

window.mainloop()
