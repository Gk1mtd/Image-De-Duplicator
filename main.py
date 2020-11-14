from tkinter import *
from PIL import ImageTk, Image

canvas_size = (500, 300)

tk_root = Tk() # creating tkinter root
tk_canvas = Canvas(tk_root, width=canvas_size[0], height=canvas_size[1]) # creating canvas
tk_canvas.pack() # marrying canvas and root

img_og = Image.open("original.png")
img_og = img_og.resize((canvas_size[0], canvas_size[1]),)
img_1 = ImageTk.PhotoImage(img_og)

tk_canvas.create_image(0, 0, anchor=NW, image=img_1)
mainloop()
