#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:12:07 2024

@author: tim
"""

import tkinter as tk

def change_foreground_color():
    # Change foreground layer color
    background_canvas.itemconfig(foreground_rectangle, fill="red")

def change_background_color():
    # Change background layer color
    background_canvas.config(bg="blue")

# Create main window
root = tk.Tk()
root.title("Background and Foreground Layers")

# Create background layer
background_canvas = tk.Canvas(root, width=400, height=300, bg="white")
background_canvas.place(x=0, y=0)
background_canvas.pack(fill=tk.BOTH, expand=True)

# Create foreground layer
foreground_canvas = tk.Canvas(root, width=400, height=300, bg="white", highlightthickness=0)
foreground_canvas.place(x=0, y=0)
foreground_canvas.pack(fill=tk.BOTH, expand=True)

# Draw some items on foreground layer
foreground_rectangle = background_canvas.create_rectangle(50, 50, 200, 150, fill="green")
foreground_label = tk.Label(foreground_canvas, text="Foreground Layer", bg="white", fg="black")
foreground_label.place(x=0, y=0)

# Create buttons to change colors
foreground_button = tk.Button(root, text="Change Foreground Color", command=change_foreground_color)
foreground_button.pack()
background_button = tk.Button(root, text="Change Background Color", command=change_background_color)
background_button.pack()

root.mainloop()