from tkinter import *
import math
from math import cos, sin, pi

window = Tk()
width = 600
centre = width/2
c = Canvas(window, width=width, height=width, bg="#FFE4E1")
c.pack()
ball = c.create_oval(centre-7, centre-7, centre+7, centre+7, fill='#C71585')
ang = 0
x2, y2 =  centre, centre

def motion():
    global ang, x2, y2, centre
    a = 2
    r = a * ang * pi
    x, y = centre, centre
    x1 = x + r *cos(ang)
    y1 = y + r *sin(ang)
    c.move(ball, x1 - x2, y1 - y2)
    point = c.create_line(x1, y1, x2, y2, fill='#FF1493')
    x2, y2 = x1, y1
    ang += 0.01
    window.after(10, motion)
 
motion()
window.mainloop()