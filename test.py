'''
Created on 23.06.2020
@author: flori
'''
import vpython as vp
import tkinter as tk

def execute(r):
    vp.box(size = vp.vector(0.5, 0.5, r), color = vp.color.red)

root = tk.Tk()
root.title("Guide")
e = tk.Entry()
b = tk.Button(command = lambda: execute(float(e.get())))

e.pack()
b.pack()

root.mainloop()
