from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image


def quitProgram(event):
    sys.exit("ShortCut Quit: Eventmessage: " + str(event))


class GUI:

    def __init__(self, windowSize, windowTitle):
        tk_root = Tk()  # creating tkinter root
        tk_root.geometry((str(windowSize[0]) + "x" + str(windowSize[1])))
        tk_root.title(windowTitle)
        # binding shortcut ctrl+q to function quitProgram()
        tk_root.bind("<Control-q>", quitProgram)

        folderpathVariable = StringVar()
        folderpathVariable.set("Folderpath is set to: Nothing yet")

        myLabel = Label(tk_root, text="Image Preview")
        myLabel.grid(row=0, column=0, columnspan=2)

        # region ImageLoading
        # loading images, resizing them
        imgOriginal = Image.open("original.png")
        imgOriginal = imgOriginal.resize((int(windowSize[0] / 2), int(windowSize[1] / 2),))
        imgOriginal = ImageTk.PhotoImage(imgOriginal)
        img_Similar = Image.open("modified.jpg")
        img_Similar = img_Similar.resize((int(windowSize[0] / 2), int(windowSize[1] / 2),))
        img_Similar = ImageTk.PhotoImage(img_Similar)
        # endregion

        # adding images to grid
        imageLabelOriginalImage = Label(image=imgOriginal)
        imageLabelOriginalImage.grid(row=1, column=0)
        imageLabelSimilarImage = Label(image=img_Similar)
        imageLabelSimilarImage.grid(row=1, column=1)

        myLabel = Label(tk_root, text="Original File")
        myLabel.grid(row=2, column=0)
        myLabel = Label(tk_root, text="Similar File")
        myLabel.grid(row=2, column=1)

        # folderpath input
        def browse_file():
            folderpath = fd.askdirectory()
            folderpathVariable.set("Folderpath is set to: " + folderpath)
            # print(self.folderpath)

        # Creating Button to search for a folderpath
        browseButton = Button(master=tk_root, text='Browse Folderpath', command=browse_file)
        browseButton.grid(row=3, column=0, columnspan=2)

        label_toFolderPath = Label(tk_root, textvariable=folderpathVariable)
        label_toFolderPath.grid(row=4, column=0, columnspan=2)

        mainloop()
