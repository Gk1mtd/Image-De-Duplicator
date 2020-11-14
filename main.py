from tkinter import *
from PIL import ImageTk, Image
from skimage.metrics import structural_similarity
from cv2 import *

canvas_size = (500, 300)

tk_root = Tk() # creating tkinter root
tk_canvas = Canvas(tk_root, width=canvas_size[0], height=canvas_size[1]) # creating canvas
tk_canvas.pack() # marrying canvas and root
# loading images, resizing them
img_1 = Image.open("original.png")
img_1 = img_1.resize((int(canvas_size[0]/2), int(canvas_size[1]/2),))
img_1 = ImageTk.PhotoImage(img_1)
img_2 = Image.open("original.png")
img_2 = img_2.resize((int(canvas_size[0]/2), int(canvas_size[1]/2),))
img_2 = ImageTk.PhotoImage(img_2)
# adding images to canvas
tk_canvas.create_image(0, 0, anchor=NW, image=img_1)
tk_canvas.create_image((int(canvas_size[0]/2)), (int(canvas_size[1]/2)), anchor=NW, image=img_2)

mainloop()

imageA = cv2.imread("original.png")
imgA_G = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
imageB = cv2.imread("original.png")
imgB_G = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)


(score, diff) = structural_similarity(imgA_G, imgB_G, full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))