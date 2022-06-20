from tkinter import *
import math
from math import *


def moving(ng, dg):   
    global n, d, x2, y2, ang, ball
    x2, y2 =  centre, centre
    ang = 0
    c.delete("all")
    ball = c.create_oval(centre-7, centre-7, centre+7, centre+7, fill='#C71585')
    if n != ng:
        n = ng
    if d != dg:
        d = dg 
    motion()


def motion():
    global ang, x2, y2, centre, n, d, ball
    if n != s1.get() or d != s2.get():
        moving(s1.get(), s2.get())
        return
    a = 200
    k = n/d
    r = a * sin(k * ang) 
    x, y = centre, centre
    x1 = x + r *cos(ang)
    y1 = y + r *sin(ang)
    c.move(ball, x1 - x2, y1 - y2)
    c.create_line(x1, y1, x2, y2, fill='#8B008B')
    x2, y2 = x1, y1
    ang += 0.01
    window.after(10, motion)
    return


window = Tk()
width = 600
centre = width/2
c = Canvas(window, width=width, height=width, bg="#FFF0F5")
c.pack()
fr = Frame(window, width=width + 1000, height=30, bg = "#DB7093")
s1 = Scale(fr, label='Setting n', from_=1, to=10, orient=HORIZONTAL, 
           length=250, resolution=1, bg = "#FFF0F5", activebackground = "#DB7093")
s2 = Scale(fr, label='Setting d', from_=1, to=10, orient=HORIZONTAL,
           length=250, resolution=1, bg = "#FFF0F5", activebackground = "#DB7093")
fr.pack()
s1.pack(side=LEFT, padx=30, pady=10)
s2.pack(side=LEFT, padx=15, pady=10)
ball = c.create_oval(centre-7, centre-7, centre+7, centre+7, fill='#C71585')
n, d = 1, 1
   
moving(n, d)
window.mainloop()