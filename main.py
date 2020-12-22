import datetime
from tkinter import *
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from image_similarity_calculator import ImageSimilarityCalculator
import glob

# Variables and Objects
pathToWorkingFolder = ""
global imageFilesInWorkingFolder
imageFilesInWorkingFolder = ""
obj_imageSimilarityCalculator = ImageSimilarityCalculator()


def listOfAllImageFiles():
    # path = 'c:\\projects\\hc2\\'
    global imageFilesInWorkingFolder
    imageFilesInWorkingFolder = ""
    imageFilesInWorkingFolder = [f for f in glob.glob(pathToWorkingFolder + "**/*.png", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpg", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpeg", recursive=True)]
    # for f in imageFilesInWorkingFolder:
    #     print(f)


def compare2Images(imageA, imageB, treshhold):  # ImageA/B should be for now a path as string to the file
    # start = datetime.datetime.now()
    obj_imageSimilarityCalculator.ssim_calculation(imageA, imageB, treshhold)
    # finish = datetime.datetime.now()
    # print(finish - start)


def startSearchForDupes():
    listOfAllImageFiles()
    for i in range(0, len(imageFilesInWorkingFolder)):
        for j in range(i, len(imageFilesInWorkingFolder)):
            # print("Compare File: " + imageFilesInWorkingFolder[i] + " with: " + imageFilesInWorkingFolder[j])
            if imageFilesInWorkingFolder[i] != imageFilesInWorkingFolder[j]:
                # print("Compare File: " + imageFilesInWorkingFolder[i] + " with: " + imageFilesInWorkingFolder[j])
                compare2Images(imageFilesInWorkingFolder[i], imageFilesInWorkingFolder[j], 0.7)

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
