from tkinter import *
from PIL import ImageTk, Image
from skimage.metrics import structural_similarity
from cv2 import *

canvas_size = (500, 300)
tk_root = Tk() # creating tkinter root
tk_canvas = Canvas(tk_root, width=canvas_size[0], height=canvas_size[1]) # creating canvas
tk_canvas.pack() # marrying canvas and root
# region ImageLoading
# loading images, resizing them
img_1 = Image.open("original.png")
img_1 = img_1.resize((int(canvas_size[0]/2), int(canvas_size[1]/2),))
img_1 = ImageTk.PhotoImage(img_1)
img_2 = Image.open("original.png")
img_2 = img_2.resize((int(canvas_size[0]/2), int(canvas_size[1]/2),))
img_2 = ImageTk.PhotoImage(img_2)
# endregion
# adding images to canvas
tk_canvas.create_image(0, 0, anchor=NW, image=img_1)
tk_canvas.create_image((int(canvas_size[0]/2)), (int(canvas_size[1]/2)), anchor=NW, image=img_2)
mainloop()

# region Image comparison
# Image comparison
imageA = cv2.imread("original.png")
imageB = cv2.imread("modified.png")

(score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
print("SSIM: {}" + str(score))
# endregion