import datetime
import glob
import json
from threading import *
from tkinter import *
from tkinter import filedialog as fd

import cv2
from skimage.metrics import structural_similarity

# Variables and Objects
global imageFilesInWorkingFolder
pathToWorkingFolder = ""
image_score_dict = {}


# Searches through the designated work path and adds all files with specific post-fix to a list
def listOfAllImageFiles():
    labelStatus.config(text="Searching for viable images 1/3")
    tk_root.update_idletasks()
    global imageFilesInWorkingFolder
    imageFilesInWorkingFolder = ""  # CLean Up of the list
    imageFilesInWorkingFolder = [f for f in glob.glob(pathToWorkingFolder + "/**/*.png", recursive=True)]
    labelStatus.config(text="Searching for viable images 2/3")
    tk_root.update_idletasks()
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "/**/*.jpg", recursive=True)]
    labelStatus.config(text="Searching for viable images 3/3")
    tk_root.update_idletasks()
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "/**/*.jpeg", recursive=True)]
    print(imageFilesInWorkingFolder)


# adds the path of imageA to the dictionary. imageA shall be the path and therefore an unique ID. this method
# is needed to access the "key" imageA and append the paths of similar images
def createNewKeyInDict(key, dict):
    dict[key] = []


# appends a value to the key of the dictionary
def addValueToDictKey(key, value, score, dict):
    dict[key].append((value, score))


def checkDictForExistingKeys(key):
    if key in image_score_dict:
        return True
    else:
        return False


def checkDictForExistingValues(value, dict):
    for i in dict.values():
        if value in i:
            return True
        else:
            return False


def dumpToJSON():
    global image_score_dict
    with open(pathToWorkingFolder + "/1_duplicates.json", 'w') as outfile:
        json.dump(image_score_dict, outfile)


# Essentially takes all the filenames in the specified folder and runs it through the imageComparison Algorithm.
# It then fills a dictionary with images and their duplicates
def startSearchForDupes():
    start = datetime.datetime.now()
    labelStatus.config(text="Start Scan")
    tk_root.update_idletasks()  # updates GUI
    imageSize = 200
    imageSize = (imageSize, imageSize)
    tk_root.update_idletasks()
    listOfAllImageFiles()
    for i in range(0, len(imageFilesInWorkingFolder)):
        # print("I-File: " + str(i+1) + " of: " + str(len(imageFilesInWorkingFolder)))
        imageA = cv2.imread(str(imageFilesInWorkingFolder[i]))
        try:
            imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            print("Color to Gray not possible: " + str(imageA) + str(e))
        try:
            imageA = cv2.resize(imageA, imageSize)
        except Exception as e:
            print("Resizing not possible: " + str(imageA) + str(e))
        for j in range(1 + i, len(imageFilesInWorkingFolder)):
            labelStatus.config(text="File: " + str(i + 1) + " of: " + str(len(imageFilesInWorkingFolder))
                                    + " | Cycle: " + str(j + 1) + " of: " + str(len(imageFilesInWorkingFolder)))
            tk_root.update_idletasks()  # updates GUI
            # print("I-File: " + str(i + 1) + " of: " + str(len(imageFilesInWorkingFolder)))
            # print("J-File: " + str(j + 1) + " of: " + str(len(imageFilesInWorkingFolder)))
            if not checkDictForExistingValues(imageFilesInWorkingFolder[j], image_score_dict):
                imageB = cv2.imread(str(imageFilesInWorkingFolder[j]))
                try:
                    imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                except Exception as e:
                    print("Color to Gray not possible: " + str(imageB) + str(e))
                try:
                    imageB = cv2.resize(imageB, imageSize)
                except Exception as e:
                    print("Resizing not possible: " + str(imageB) + str(e))
                try:
                    (score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
                except Exception as e:
                    print("Error checking for similarities" + str(e))
                if not checkDictForExistingKeys(imageFilesInWorkingFolder[i]):
                    createNewKeyInDict(imageFilesInWorkingFolder[i], image_score_dict)
                addValueToDictKey(imageFilesInWorkingFolder[i], imageFilesInWorkingFolder[j], score, image_score_dict)

                finish = datetime.datetime.now()
                labelTimeLeft.config(text="Time spend: " + str(finish - start))
                tk_root.update_idletasks()  # updates GUI
                labelStatus.config(text="Task Done in: " + pathToWorkingFolder)
                tk_root.update_idletasks()  # updates GUI
    dumpToJSON()
    finish = datetime.datetime.now()
    # print(finish - start)
    labelTimeLeft.config(text="Total Time: " + str(finish - start))
    tk_root.update_idletasks()  # updates GUI


# Quit Program with shortcut
def quitProgram(event):
    sys.exit("ShortCut Quit: Event Message: " + str(event))


def choseFolder():
    global pathToWorkingFolder
    pathToWorkingFolder = fd.askdirectory()
    # print(pathToWorkingFolder)
    labelStatus.config(text="Folder Selected: " + pathToWorkingFolder)
    tk_root.update_idletasks()


def startSearchThreading():
    t1 = Thread(target=startSearchForDupes)
    t1.start()


# GUI
# tk root
tk_root = Tk()
tk_root.geometry("450x120")
tk_root.bind("<Control-q>", quitProgram)  # binding shortcut ctrl+q to function quitProgram()
tk_root.title("DeDup 1.0")
# Gets both half the screen width/height and window width/height
positionRight = int((tk_root.winfo_screenwidth() / 2) - tk_root.winfo_reqwidth())
positionDown = int((tk_root.winfo_screenheight() / 2) - tk_root.winfo_reqheight())
# Positions the window in the center of the page.
tk_root.geometry("+{}+{}".format(positionRight, positionDown))

# Buttons
choseFolder = Button(tk_root, text="Chose Folder", command=choseFolder)
startScan = Button(tk_root, text="Start Scan", command=startSearchThreading)

# Label
labelHeadline = Label(tk_root, text="Image Dedup by Image Content")
labelStatus = Label(tk_root, text="Not in progress")
labelTimeLeft = Label(tk_root, text="Time Spend")

# packing
labelHeadline.pack()
choseFolder.pack()
startScan.pack()
labelStatus.pack()
labelTimeLeft.pack()

# GUI loop
mainloop()
