import tkinter

root = tkinter.Tk()
frame = tkinter.Frame(root,height=500,width=500)

def key_handler(event):
    print("clicked!")
    #print(event.char, event.keysym, event.keycode)

frame.bind("<KeyPress>", key_handler)
frame.bind("<Button-1>", key_handler)
frame.pack()
frame.focus_set()
root.mainloop()