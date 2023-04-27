from tkinter import *
import random
import time

tk = Tk()
tk.title = "Game"
tk.restizable(0,0)
tk.wm_attributees("-topmost", 1)

canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
    def draw(self):
        pass

ball = Ball(canvas, "red")


def draw(self):
    self.canvas.move(self.id, 0, -1)
    
while 1:
    ball.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
    
tk.mainloop()