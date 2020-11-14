from tkinter import *
from PIL import ImageTk, Image

tk_root = Tk()
tk_canvas = Canvas(tk_root, width=900, height=500)
tk_canvas.pack()
img_1 = ImageTk.PhotoImage(Image.open("original.png"))
tk_canvas.create_image(20, 20, anchor=NW, image=img_1)
mainloop()
