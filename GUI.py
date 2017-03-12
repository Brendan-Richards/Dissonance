from tkinter import *


def guiInit(vals):
    master = Tk()

    l1 = Label(master, text="cutoff:")
    e1 = Entry(master)
    l2 = Label(master, text="min peak height:")
    e2 = Entry(master)
    l3 = Label(master, text="min peak distance:")
    e3 = Entry(master)
    l4 = Label(master, text="Low:")
    e4 = Entry(master)
    l5 = Label(master, text="High:")
    e5 = Entry(master)

    l1.pack()
    e1.pack()
    l2.pack()
    e2.pack()
    l3.pack()
    e3.pack()
    l4.pack()
    e4.pack()
    l5.pack()
    e5.pack()


    def update():
        vals[0] = float(e1.get())
        vals[1] = float(e2.get())
        vals[2] = float(e3.get())
        vals[3] = float(e4.get())
        vals[4] = float(e5.get())
        vals[5] = False
        master.destroy()

    def save():
        vals[0] = float(e1.get())
        vals[1] = float(e2.get())
        vals[2] = float(e3.get())
        vals[3] = float(e4.get())
        vals[4] = float(e5.get())
        vals[5] = True
        master.destroy()

    b1 = Button(master, text="Redraw", command=update)
    b1.pack()

    b2 = Button(master, text="Save", command=save)
    b2.pack()

    e1.insert(END, str(vals[0]))
    e2.insert(END, str(vals[1]))
    e3.insert(END, str(vals[2]))
    e4.insert(END, str(vals[3]))
    e5.insert(END, str(vals[4]))

    mainloop()

# asdf = [.1, .05, 10000, 400, 1000, False]
# print(asdf)
# guiInit(asdf)
# print(asdf)