from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from image_similarity_calculator import ImageSimilarityCalculator

# canvas_size = (500, 300)
# tk_root = Tk()  # creating tkinter root
# tk_canvas = Canvas(tk_root, width=canvas_size[0], height=canvas_size[1])  # creating canvas
# tk_canvas.pack()  # marrying canvas and root
# # region ImageLoading
# # loading images, resizing them
# img_1 = Image.open("original.png")
# img_1 = img_1.resize((int(canvas_size[0] / 2), int(canvas_size[1] / 2),))
# img_1 = ImageTk.PhotoImage(img_1)
# img_2 = Image.open("original.png")
# img_2 = img_2.resize((int(canvas_size[0] / 2), int(canvas_size[1] / 2),))
# img_2 = ImageTk.PhotoImage(img_2)
# # endregion
# # adding images to canvas
# tk_canvas.create_image(0, 0, anchor=NW, image=img_1)
# tk_canvas.create_image((int(canvas_size[0] / 2)), (int(canvas_size[1] / 2)), anchor=NW, image=img_2)
#
#
# # folderpath input
# def browse_file():
#     new_path = fd.askdirectory()
#     print(new_path)
#
# browseButton = Button(master=tk_root, text='Browse', width=6, command=browse_file)
# browseButton.pack()
#
# mainloop()

# to calculate SSIM (similarity) of to pictures given as setImageA() and setImageB()
obj_imageSimilarityCalculator = ImageSimilarityCalculator()
obj_imageSimilarityCalculator.ssim_calculation("other_image.jpg", "modified.jpg")