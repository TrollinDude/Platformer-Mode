from tkinter import *
import tkinter
import _thread

toggled = 0

def main(useless1,useless2):

    def changestate():
        global toggled
        if toggled == 1:
            toggled = 0
        else: toggled = 1

    top = tkinter.Tk()
    C1 = Checkbutton(top, text = "test", command=changestate)
    C1.grid()

    top.mainloop()

_thread.start_new_thread(main, (1,1))

while True:
    try:
        print(toggled)
    except:
        ()