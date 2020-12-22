import datetime
from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from image_similarity_calculator import ImageSimilarityCalculator
import glob

# Variables and Objects
pathToWorkingFolder = ""
imageFilesInWorkingFolder = ""
obj_imageSimilarityCalculator = ImageSimilarityCalculator()


def listOfAllImageFiles():
    # path = 'c:\\projects\\hc2\\'
    imageFilesInWorkingFolder = ""
    imageFilesInWorkingFolder = [f for f in glob.glob(pathToWorkingFolder + "**/*.png", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpg", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpeg", recursive=True)]
    for f in imageFilesInWorkingFolder:
        print(f)


def compare2Images(imageA, imageB):  # ImageA/B should be for now a path as string to the file
    # start = datetime.datetime.now()
    obj_imageSimilarityCalculator.ssim_calculation(imageA, imageB)
    # finish = datetime.datetime.now()
    # print(finish - start)


def startSearchForDupes():
    listOfAllImageFiles()


# GUI
def setPathToWorkingDirectory():
    global pathToWorkingFolder
    pathToWorkingFolder = fd.askdirectory()
    print("Set Working Directory to: " + pathToWorkingFolder)


def quitProgram(event):
    sys.exit("ShortCut Quit: Eventmessage: " + str(event))


tk_root = Tk()
tk_root.bind("<Control-q>", quitProgram)  # binding shortcut ctrl+q to function quitProgram()
tk_root.title("DeDup 0.1")
buttonToSetPathToWorkingFolder = Button(tk_root, text="Set Path To Working Directory",
                                        command=setPathToWorkingDirectory)
buttonToSetPathToWorkingFolder.grid(row=0, column=0)
buttonStartSearchForDupes = Button(tk_root, text="Start Search For Dupes", command=startSearchForDupes)
buttonStartSearchForDupes.grid(row=1, column=0)

mainloop()
