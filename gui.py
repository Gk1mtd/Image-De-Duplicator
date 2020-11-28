from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image


class GUI:
    def quit(self, event):
        sys.exit("ShortCut Quit")

    def __init__(self, windowSize, windowTitle):
        tk_root = Tk()  # creating tkinter root
        tk_root.geometry((str(windowSize[0]) + "x" + str(windowSize[1])))
        tk_root.title(windowTitle)
        tk_root.bind("<Control-q>", self.quit)

        # myLabels = []
        # for i in range(5):
        #     print("Start")
        #     myLabels.append(Label(tk_root, text="BLAAAAAAA"))
        #     myLabels[i].pack()
        myLabel = Label(tk_root, text="Image Preview")
        myLabel.grid(row=0, column=0, columnspan=2)

        tk_canvas = Canvas(tk_root, width=windowSize[0], height=windowSize[1] / 2)  # creating canvas
        tk_canvas.grid(row=1, column=0, columnspan=2)  # marrying canvas and root

        # region ImageLoading
        # loading images, resizing them
        img_1 = Image.open("original.png")
        img_1 = img_1.resize((int(windowSize[0] / 2), int(windowSize[1] / 2),))
        img_1 = ImageTk.PhotoImage(img_1)
        img_2 = Image.open("original.png")
        img_2 = img_2.resize((int(windowSize[0] / 2), int(windowSize[1] / 2),))
        img_2 = ImageTk.PhotoImage(img_2)
        # endregion

        # adding images to canvas
        tk_canvas.create_image(0, 0, anchor=NW, image=img_1)
        tk_canvas.create_image((int(windowSize[0] / 2)), 0, anchor=NW, image=img_2)

        myLabel = Label(tk_root, text="Original File")
        myLabel.grid(row=2, column=0)
        myLabel = Label(tk_root, text="Similar File")
        myLabel.grid(row=2, column=1)

        # folderpath input
        def browse_file():
            new_path = fd.askdirectory()
            print(new_path)

        # Creating Button to search for a folderpath
        browseButton = Button(master=tk_root, text='Browse Folderpath', command=browse_file)
        browseButton.grid(row=3, column=0, columnspan=2)

        mainloop()
