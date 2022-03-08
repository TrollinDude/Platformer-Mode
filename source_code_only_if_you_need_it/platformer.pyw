import os
running = True
if not os.path.exists('config.txt'):
    print('config.txt does not exist! im creating it')
    with open('config.txt', 'a') as f:
        f.write('smoothing_iterations 10\nfps 60\n#smooting_iterations default is 10 and this value changes the way the movement smoothing works\n#the default fps is 60 and increasing this will make the program run faster allowing you to use higher fps in gd but this is at the cost of cpu usage')
        f.close()
    smooth_iter_c = 10
    loop_sleep = 0.0001
    fps = 60
else:
    try:
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        fps = int(splitted2[1])
    except:
        print('something is wrong in your config,\nill reset it rq')
        with open('config.txt', 'w+') as f:
            f.truncate(0)
            f.write('smoothing_iterations 10\nfps 60\n#smooting_iterations default is 10 and this value changes the way the movement smoothing works\n#the default fps is 60 and increasing this will make the program run faster allowing you to use higher fps in gd but this is at the cost of cpu usage')
            f.close()
        smooth_iter_c = 10
        loop_sleep = 0.0001
        fps = 60

smooth_iter_c = 10
loop_sleep = 0.0001

import keyboard as k
import time
from sys import exit as sysexit
import time
from pygdmod.pygdmod import *
from requests import get as requestsget
import tkinter as tk
from tkinter import ttk
import _thread
import webbrowser
from pygame import time as clockt

#Gui
toggled = 0
toggled2 = 0

def main(useless1,useless2):
    global window
    global slider
    global speedhacklbl
    def changestate():
        global toggled
        global xpos
        if toggled == 1:
            toggled = 0
        else:  
            xpos = modloader.getXpos(1)
            toggled = 1

    def changestate2():
        global toggled2
        global xposp1, xposp2
        if toggled2 == 1:
            toggled2 = 0
        else:  
            xposp1 = modloader.getXpos(1)
            xposp2 = modloader.getXpos(2)
            toggled2 = 1

    def reloadsettings():
        global smooth_iter_c
        global loop_sleep
        global fps
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        fps = int(splitted2[1])
        updatestatus.config(text="Setting Synced From config.txt")

    window = tk.Tk()
    window.geometry('300x110')
    window.resizable(False, False)
    window.title('Platformer Mode')

    C1 = tk.Checkbutton(window, text = "Toggle Platformer Mode", command=changestate)
    C1.place(relx=.3, rely= .1, anchor = "center")

    C2 = tk.Checkbutton(window, text = "Toggle 2p Mode", command=changestate2)
    C2.place(relx=.8, rely= .1, anchor = "center")


    speedhackval = tk.DoubleVar()
    slider = ttk.Scale(window,from_=0,to=2,orient='horizontal')
    slider.place(relx=.5, rely=.3)

    spdhck=" "
    speedhacklbl = tk.Label(window, text=(spdhck))
    speedhacklbl.place(relx=.3, rely=.4, anchor="center")

    chckupdate = tk.Button(window, text="Check For Update", command = checkforupdate)
    chckupdate.place(relx=.3, rely=.7, anchor="center")

    ReSyncset = tk.Button(window, text="Reload config.txt", command = reloadsettings)
    ReSyncset.place(relx=.7, rely=.7, anchor="center")

    global updatestatus
    updatestatus = tk.Label(window, text=" ")
    updatestatus.place(relx=.5, rely=.92, anchor="center")

    def close_window():
        global running
        running = False 

    window.protocol("WM_DELETE_WINDOW", close_window)

    window.mainloop()

#end of gui

current_ver = 4

def callback(url):
    webbrowser.open_new(url)

def checkforupdate():
    global updatestatus

    try: updatestatus.config(text="Checking For Updates...") 
    except: ()

    try:
        r = requestsget('https://pastebin.com/raw/5KxfejCf', allow_redirects=True)
        if int(r.text.splitlines()[0]) != current_ver:
            textt = "Out of date version. Click here"
            try: 
                updatestatus.config(text=str(textt), fg="blue", cursor="hand2") 
                updatestatus.bind("<Button-1>", lambda e: callback("https://github.com/TrollinDude/Platformer-Mode/releases"))
            except:()
        else:
            try: updatestatus.config(text="You are running the latest version")
            except:()
    except:
        updatestatus.config(text="Failed to check for updates!")

loop_init = False
xpos = 0
xposp1 = 0
xposp2 = 0
once = 1
once1 = 1
Clock = clockt.Clock()
try:
    modloader = GeometryDashModloader()
except:
    print("geometry dash not found")
    input()
    sysexit()
step = 0
prev_time = time.time()
checkpoints = [1]
nocheckpoint = 1
was_pressed_d = False
was_pressed_a = False
was_pressed_d1 = False
was_pressed_a1 = False
was_pressed_d2 = False
was_pressed_a2 = False

_thread.start_new_thread(main, (1,1))
speedhackval = 1

while True:
    speedhack = modloader.getSpeedhack()

    '''
    Controls check
    '''
    if k.is_pressed("d") or k.is_pressed("right") and not isDead and toggled2 == 0:
        xpos += step * dt * 60 * speedhack
        was_pressed_d = True
        smooth_iter = smooth_iter_c
    elif was_pressed_d:
        try:
            xpos += smooth_iter * dt * 60 * speedhack / smooth_iter
        except:
            was_pressed_d = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_d = False

    if k.is_pressed("a") or k.is_pressed("left") and not isDead and toggled2 == 0:
        xpos -= step * dt * 60 * speedhack
        was_pressed_a = True
        smooth_iter = smooth_iter_c
    elif was_pressed_a:
        try:
            xpos -= smooth_iter * dt * 60 * speedhack / smooth_iter
        except:
            was_pressed_a = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_a = False


    if k.is_pressed("d") and not isDead and toggled2 == 1:
        xposp1 += step * dt * 60 * speedhack
        was_pressed_d1 = True
        smooth_iter1 = smooth_iter_c
    elif was_pressed_d1 and toggled2 == 1:
        try:
            xposp1 += smooth_iter1 * dt * 60 * speedhack / smooth_iter1
        except:
            was_pressed_d1 = False
        smooth_iter1 -= 1
        if smooth_iter1 == 1:
            was_pressed_d1 = False

    if k.is_pressed("a") and not isDead and toggled2 == 1:
        xposp1 -= step * dt * 60 * speedhack
        was_pressed_a1 = True
        smooth_iter1 = smooth_iter_c
    elif was_pressed_a1 and toggled2 == 1:
        try:
            xposp1 -= smooth_iter1 * dt * 60 * speedhack / smooth_iter1
        except:
            was_pressed_a1 = False
        smooth_iter1 -= 1
        if smooth_iter1 == 1:
            was_pressed_a1 = False

    if k.is_pressed("right") and not isDead and toggled2 == 1:
        xposp2 += step * dt * 60 * speedhack
        was_pressed_d2 = True
        smooth_iter2 = smooth_iter_c
    elif was_pressed_d2 and toggled2 == 1:
        try:
            xposp2 += smooth_iter2 * dt * 60 * speedhack / smooth_iter2
        except:
            was_pressed_d2 = False
        smooth_iter2 -= 1
        if smooth_iter2 == 1:
            was_pressed_d2 = False

    if k.is_pressed("left") and not isDead and toggled2 == 1:
        xposp2 -= step * dt * 60 * speedhack
        was_pressed_a2 = True
        smooth_iter2 = smooth_iter_c
    elif was_pressed_a2 and toggled2 == 1:
        try:
            xposp2 -= smooth_iter2 * dt * 60 * speedhack / smooth_iter2
        except:
            was_pressed_a2 = False
        smooth_iter2 -= 1
        if smooth_iter2 == 1:
            was_pressed_a2 = False

    now = time.time()
    dt = now - prev_time
    prev_time = now

    if modloader.isInEndscreen():
        checkpoints = []
        xpos = 1

    isDead = modloader.isDead()
    val6 = modloader.getPlayerSpeed()
    xposval = modloader.getXpos() # player 1 by default

    if xposval == 0:
        xpos = 1
        checkpoints = []

    #make it work in practice
    try:   
        if k.is_pressed("z") and once1 == 1 and modloader.isInPracticeMode():
            checkpoints.append([xpos, xposp1, xposp2])
            nocheckpoint = 0
            once1 = 0
        if k.is_pressed("z") == False and once1 == 0 and modloader.isInPracticeMode():
            once1 = 1

        if k.is_pressed("x") and once == 1 and modloader.isInPracticeMode():
            checkpoints.pop()
            once = 0
        if k.is_pressed("x") == False and once == 0 and modloader.isInPracticeMode():
            once = 1
    except:
        nocheckpoint = 1

    #respawning on check points
    if not isDead and toggled == 1 and toggled2 == 0:
        modloader.setXpos(pos=xpos, player='both') # set xpos of both players
    if isDead and toggled == 1 and toggled2 == 0:
        try:
            xpos = checkpoints[-1][0]
        except:
            ()
        if nocheckpoint == 1:
            xpos = 1

    if not isDead and toggled == 1 and toggled2 == 1:
        modloader.setXpos(pos=xposp1, player=1)
        modloader.setXpos(pos=xposp2, player=2)
    if isDead and toggled == 1 and toggled2 == 1:
        try:
            xposp1 = checkpoints[-1][1]
            xposp2 = checkpoints[-1][2]
        except:
            ()
        if nocheckpoint == 1:
            xposp1 = 1
            xposp2 = 1

    if xpos <= 0:
        xpos = 0
        xposp1 = 0
        xposp2 = 0

    if val6 == 0.699999988079071:
        step = 4.186001
    elif val6 == 0.8999999761581421:
        step = 5.193001747
    elif val6 == 1.100000023841858:
        step = 6.457002163
    elif val6 == 1.2999999523162842:
        step = 7.800002098
    elif val6 == 1.600000023841858:
        step = 9.600003242
    else:
        step = 4.186001

    if slider.get() != 0:
        speedhackval = slider.get()
        try:
            modloader.setSpeedHack(float(round(speedhackval, 1)))
        except:
            ()
        spdhck = "Set Speedhack: " + str(round(speedhackval, 1))
        speedhacklbl.config(text=str(spdhck))
    if loop_init == False:
        speedhacklbl.config(text="Set Speedhack: 1")
        modloader.setSpeedHack(1)

    if running == False:
        sysexit()

    loop_init = True
    Clock.tick(fps)