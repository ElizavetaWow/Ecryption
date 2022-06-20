from tkinter import *
import math
from math import *

def start():
    global balls
    
    def moving():
        i = 0
        for jj in range(k):
            for j in range(l):
                if jj == 0 and j == 0:
                    a, b = 1, 1
                    c.move(balls[i][1], 0,-1000)
                    c.move(balls[i][2], -1000, 0)
                elif jj == 0:
                    a, b = j, j
                    c.move(balls[i][2], -1000, 0)
                elif j == 0:
                    a, b = jj, jj
                    c.move(balls[i][1], 0,-1000)
                else:
                    a, b = j, jj
                dx = ampl * sin(b * balls[i][5])
                dy = ampl * sin(a * balls[i][5] + q)
                c.move(balls[i][0], dx - balls[i][3], dy - balls[i][4])
                c.move(balls[i][1], dx - balls[i][3], dy - balls[i][4])
                c.move(balls[i][2], dx - balls[i][3], dy - balls[i][4])
                x = c.coords(balls[i][0])[0] + 7
                y = c.coords(balls[i][0])[1] + 7
                if balls[i][5] <  2 * pi and balls[i][5] < 2 * pi:
                    c.create_line(x, y, x + dx - balls[i][3], y + dy - balls[i][4], fill='white')
                balls[i][3], balls[i][4], balls[i][5] = dx, dy,  balls[i][5] + pi/62
                i += 1 
    k = width // (ampl * 2) - 1
    l = height // (ampl * 2) - 1 
    rk = (width - k *  100) // (k + 1)
    rl = (height - l * 100) // (l + 1)
    for x in range(k):  
        for y in range(l):
            create_ball(ampl + x * 100 + rk * (x + 1), ampl + y * 100 + rl * (y + 1))   
    motion(moving)
        
def create_ball(x, y):
    ball = c.create_oval(x-7, y-7, x+7, y+7, fill='white')
    c.move(ball, 0, ampl)
    balls.append([ball, c.create_line(-width, y + ampl, width * 2, y + ampl, fill = "white"),
                  c.create_line(x, -height,  x, height * 2, fill = "white"), 0, ampl, 0])
    
def motion(act):
    def motion_move():
        act()
        window.after(1, motion_move)

    return motion_move()

    
window = Tk()
ampl = 50
width = 700
height = 700
c = Canvas(window, width = width, height = height, bg="black")
c.pack()
balls = []
k = 0
q = pi/2

start()
window.mainloop()