
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
#from PIL.ImageTk import PhotoImage
def hexToVec(hex) : 
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def create_alphaPoly(self,images,*args, **kwargs):
    if "alpha" in kwargs:         
        if "fill" in kwargs:
            # Get and process the input data
            #print(kwargs["fill"])# = "blue"
            #kwargs["fill"] = "#d466a1"
            fill = hexToVec(kwargs.pop("fill"))\
                   + (int(kwargs.pop("alpha") * 255),)
            outline = kwargs.pop("outline") if "outline" in kwargs else None

            # We need to find a rectangle the polygon is inscribed in
            # (max(args[::2]), max(args[1::2])) are x and y of the bottom right point of this rectangle
            # and they also are the width and height of it respectively (the image will be inserted into
            # (0, 0) coords for simplicity)
            image = Image.new("RGBA", (max(args[::2]), max(args[1::2])))
            ImageDraw.Draw(image).polygon(args, fill=fill, outline=outline)

            images.append(ImageTk.PhotoImage(image))  # prevent the Image from being garbage-collected
            return self.create_image(0, 0, image=images[-1], anchor="nw")  # insert the Image to the 0, 0 coords
        raise ValueError("fill color must be specified!")
    return self.create_polygon(*args, **kwargs)
"""

images = []  # to hold the newly created image(s)        

root = Tk()
frame = Frame(root)
frame.grid(row=0, column=0)
frame.pack()
canvas = Canvas(width=260, height=310)
def erase() :
    canvas.delete(i)
but2 = Button(frame, text="erase", command=erase)

but2.grid(row=1,column=0)
but2.pack()
canvas.pack()

i = create_polygonWithAlpha(root, canvas , images, 10, 10, 10, 20, 200, 300, 250, 150, 10, 10, fill="blue", alpha=0.5)
create_polygonWithAlpha(root,canvas,images,150, 100, 200, 120, 240, 180, 210, 200, 150, 150, 100, 200, fill="blue", alpha=0.2)

root.mainloop()
"""