import keyboard, time, os
import ctypes
from tkinter import *
from functools import partial
from sendInput import PressKey, ReleaseKey
from convertInputs import convert
from pathlib import Path

time_ = 0
bg = ""
stopkey = "r"

f_ = open(str(Path(__file__).parent.parent) + "/info.txt", "r")
for line in f_:
    if line.startswith("time"):
        time_ = line[5]
        continue
    if line.startswith("stop_key"):
        stopkey = line[9]
        continue
    if line.startswith("bg"):
        bg = line.split("=")[1]
        bg = bg[:-1]
        break

SendInput = ctypes.windll.user32.SendInput


def insertButtons(frame):
    folder = str(Path(__file__).parent.parent) + "/songs/"
    files = os.listdir(folder)
    n = len(files)
    x = 1
    y = 1

    for file in files:
        t = str(file)
        if t.endswith(".txt"):
            t = t[:-4]
        else:
            t = "404 error"

        button = Button(frame, width=21, text=t, command=partial(click, folder + t)).grid(row=y, column=x)

        Label(frame, bg=bg, text=" ").grid(row=y, column=x + 1)
        x = x + 2
        if x > 6:
            x = 1
            Label(frame, bg=bg, text=" ", pady=0).grid(row=y + 1, column=1)
            y = y + 2


def click(t):
    if t == "404 error":
        return
    time.sleep(float(time_))
    file = open(t + ".txt", "r")
    bpm = 0
    speed = 1

    for line in file:
        if line.startswith("BPM:"):
            bpm = int(line.split("BPM:")[1])
            continue
        if line.startswith("SPEED:"):
            speed = float(line.split("SPEED:")[1])
            continue

        line = line.split(" ")
        for note in line:
            if keyboard.is_pressed(stopkey):
                break
            if len(note) > 1:
                for i in note:
                    play(i)
                time.sleep(60 / speed / bpm)
            else:
                if note != "\n" and note != "" and note != " " and play(note) == 1:
                    time.sleep(60 / speed / bpm)


def play(x):
    x = x.lower()
    if not isinstance(x, str):
        return 0
    x = convert(x)
    if x == 0:
        return 0
    if x == 1:
        return 1
    PressKey(x)
    time.sleep(2/60)
    ReleaseKey(x)
    return 1


root = Tk()
root.iconbitmap("icon.ico")
root.title("Genshin Impact lire player")
root.geometry("510x500")
root.resizable(0, 0)
root.configure(background=bg)

Header = Label(root, text="made by 02_t", font=("Arial", 16), bg=bg, fg="#a0a0ad").pack()
text1 = Label(root,
              text="Click on the song you want played and switch to genshin,\n your song will be played in " + str(
                  time_) + " seconds. Press R to stop the song.",
              font=("Calibri", 12), bg=bg, fg="#6e6e7d").pack()

frame = Frame(root, bg=bg, height="412", width="480")
insertButtons(frame)
frame.place(x=10, y=85)

root.mainloop()
