#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:41:36 2024

@author: tim
"""

import tkinter as tk

def move_rectangle():
    # Change the coordinates of the rectangle
    canvas.coords(rectangle, x1 + 10, y1 + 10, x2 + 10, y2 + 10)

root = tk.Tk()
root.title("Move Rectangle")

canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Coordinates of the rectangle
x1, y1, x2, y2 = 50, 50, 100, 100

# Create a rectangle on the canvas
rectangle = canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

# Create a button to move the rectangle
button = tk.Button(root, text="Move Rectangle", command=move_rectangle)
button.pack()
def dele() :
    canvas.delete(rectangle)
but2 = tk.Button(root, text="del Rectangle", command=dele)
but2.pack()
root.mainloop()

