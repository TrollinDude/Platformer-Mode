import os

if not os.path.exists('config.txt'):
    print('config.txt does not exist! im creating it')
    with open('config.txt', 'a') as f:
        f.write('smoothing_iterations 10\nloop_sleep_time 0.0001') #when making updates change this version number
        f.close()
    print('PLEASE READ THIS! PLEASE READ THIS!')
    print('config created,\nyou can configure the smoothing steps in it,\nby default its 10, you can set the value to something bigger if you want it to be smoother,\nor set it to 0 if you dont want any movement smoothing\n\nloop sleep time means how much program will do nothing in the loop. if you expierence jitter while standing in place, make it smaller or 0.')
    smooth_iter_c = 10
    loop_sleep = 0.0001
else:
    try:
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        loop_sleep = float(splitted2[1])
        print('smoothing iterations:', smooth_iter_c)
        print('loop sleep time:', loop_sleep)
    except:
        print('something is wrong in your config,\nill reset it rq')
        with open('config.txt', 'w+') as f:
            f.truncate(0)
        f.write('smoothing_iterations 10\nloop_sleep_time 0.0001')
        f.close()
        smooth_iter_c = 10
        loop_sleep = 0.0001
        print('smoothing iterations:', smooth_iter_c)
        print('loop sleep time:', loop_sleep)

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

#Gui
toggled = 0

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

    def reloadsettings():
        global smooth_iter_c
        global loop_sleep
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        loop_sleep = float(splitted2[1])
        updatestatus.config(text="Setting Synced From config.txt")

    window = tk.Tk()
    window.geometry('300x100')
    window.resizable(False, False)
    window.title('Platformer Mode')

    C1 = tk.Checkbutton(window, text = "Toggle Platformer Mode", command=changestate)
    C1.place(relx=.5, rely= .1, anchor = "center")

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

    window.mainloop()

#end of gui

current_ver = 3

def callback(url):
    webbrowser.open_new(url)

def checkforupdate():
    global updatestatus

    try: updatestatus.config(text="Checking For Updates...") 
    except: ()

    try:
        r = requestsget('https://pastebin.com/raw/43PcML6z', allow_redirects=True)
        if int(r.text.splitlines()[0]) != current_ver:
            textt = "You are using a out of date version. Click here to download the newest version"
            try: 
                updatestatus.config(text=str(textt), fg="blue", cursor="hand2") 
                updatestatus.bind("<Button-1>", lambda e: callback("https://github.com/TrollinDude/pl_mode/releases"))
            except:()
        else:
            try: updatestatus.config(text="You are running the latest version")
            except:()
    except:
        print('Failed to check for updates!!!!')

loop_init = False
xpos = 0
once = 1
once1 = 1
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


print('injected with base', hex(modloader.getBaseAddress()),'pid:', hex(modloader.getProcessId()))

_thread.start_new_thread(main, (1,1))
speedhackval = 1
while True:
    speedhack = modloader.getSpeedhack()

    '''
    Controls check
    '''
    if k.is_pressed("d") or k.is_pressed("right") and not isDead:
        xpos += step * dt * 60 * speedhack
        was_pressed_d = True
        smooth_iter = smooth_iter_c
    elif was_pressed_d:
        try:
            xpos += smooth_iter * dt * 60 / speedhack / smooth_iter
        except:
            was_pressed_d = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_d = False

    if k.is_pressed("a") or k.is_pressed("left") and not isDead:
        xpos -= step * dt * 60 * speedhack
        was_pressed_a = True
        smooth_iter = smooth_iter_c
    elif was_pressed_a:
        try:
            xpos -= smooth_iter * dt * 60 / speedhack/smooth_iter
        except:
            was_pressed_a = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_a = False

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
            checkpoints.append(xpos)
            nocheckpoint = 0
            once1 = 0
        else:
            once1 = 1

        if k.is_pressed("x") and once == 1 and modloader.isInPracticeMode():
            checkpoints.pop()
            once = 0
        else:
            once = 1
    except:
        nocheckpoint = 1

    #respawning on check points
    if not isDead and toggled == 1:
        modloader.setXpos(pos=xpos, player='both') # set xpos of both players
    else:
        try:
            xpos = checkpoints[-1]
        except:
            pass
        if nocheckpoint == 1:
            xpos = 1

    if xpos <= 0:
        xpos = 0

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

    # not hog cpu
    loop_init = True
    time.sleep(loop_sleep)