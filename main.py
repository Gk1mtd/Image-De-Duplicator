# Eigentlich sollte ich die Score Daten in einer Datenbank speichern SQLite z.B.
# damit könnte zu jedem Bild-zu-Bild vergleich der Score gespeichert werden und damit Rechenzeit optimiert
# da die selben Bilder nicht n^n mal verglichen werden müssen
# import datetime
# from time import sleep
import _thread
import datetime
import multiprocessing
from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import Progressbar
# import cv2
from PIL import ImageTk, Image
from image_similarity_calculator import ImageSimilarityCalculator
import glob
import pprint
import json

# Variables and Objects
pathToWorkingFolder = ""
global imageFilesInWorkingFolder
image_score_dict = {}
obj_imageSimilarityCalculator = ImageSimilarityCalculator()


# Searches through the designated work path and adds all files with specific post-fix to a list
def listOfAllImageFiles():
    # path = 'c:\\projects\\hc2\\'
    global imageFilesInWorkingFolder
    imageFilesInWorkingFolder = ""  # CLean Up of the list
    imageFilesInWorkingFolder = [f for f in glob.glob(pathToWorkingFolder + "**/*.png", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpg", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpeg", recursive=True)]
    # for f in imageFilesInWorkingFolder:
    #     print(f)


# uses the image-similarity_calculator to check two images against each other, outputs teh score and the paths to the files
def compare2Images(imageA, imageB):  # ImageA/B are paths, as string, to the specified files
    score, pathToA, pathToB = obj_imageSimilarityCalculator.ssim_calculation(imageA, imageB)
    return [score, pathToA, pathToB]


# adds the path of imageA to the dictionary. imageA shall be the path and therefore an unique ID. this method
# is needed to access the "key" imageA and append the paths of similar images
def createNewKeyInDict(image_A):
    global image_score_dict
    image_score_dict[image_A] = []


# resets the dict to nothing
def clearDict():
    global image_score_dict
    image_score_dict = {}


# appends a value to the key of the dictionary
def addValueToDictKey(image_A, similar_file_B):
    global image_score_dict
    image_score_dict[image_A].append(similar_file_B)
    # print("Added a new Value for Key: " + str(image_A) + " Value: " + str(similar_file_B))
    # pprint.pprint(image_score_dict)


def checkDictForExistingKeys(key):
    global image_score_dict
    if key in image_score_dict:
        return True
    else:
        return False


def checkDictForExistingValues(value):
    global image_score_dict
    for i in image_score_dict.values():
        if value in i:
            return True
        else:
            return False


def dumpToJSON():
    global image_score_dict
    with open('data.json', 'w') as outfile:
        json.dump(image_score_dict, outfile)


def startThread():
    _thread.start_new_thread(startSearchForDupes, ("test1",))

def startSearchForDupes(threadname="bla"):
    listOfAllImageFiles()
    threshold = float(thresholdTextfield.get())/100
    similarImagesCounter = 0
    #start = datetime.datetime.now()
    for i in range(0, len(imageFilesInWorkingFolder)):
        #print("\n### File batch #: " + str(i + 1) + " of " + str(len(imageFilesInWorkingFolder)) + " is processed.")
        for j in range(0 + i + 1, len(imageFilesInWorkingFolder)):
            if not checkDictForExistingValues(imageFilesInWorkingFolder[j]):
                score, pathToA, pathToB = compare2Images(imageFilesInWorkingFolder[i], imageFilesInWorkingFolder[j])
                if score >= threshold:
                    if not checkDictForExistingKeys(imageFilesInWorkingFolder[i]):
                        createNewKeyInDict(imageFilesInWorkingFolder[i])
                        similarImagesCounter +=1
                    addValueToDictKey(pathToA, pathToB)
            progressBarj['value'] = (100 * (j-i)) / (len(imageFilesInWorkingFolder)-i)  # shows single file progress
            tk_root.update_idletasks()  # updates GUI
        progressBari['value'] = ((100 * (i + 1)) / len(imageFilesInWorkingFolder))  # shows total Progress
        tk_root.update_idletasks()  # updates GUI
    dumpToJSON()
    labelSimilarImagesFound.config(text=str(similarImagesCounter))
    #pprint.pprint(image_score_dict)
    #finish = datetime.datetime.now()
    #print(finish - start)


# GUI
def setPathToWorkingDirectory():
    global pathToWorkingFolder
    pathToWorkingFolder = fd.askdirectory() + "/"
    print("Set Working Directory to: " + pathToWorkingFolder)
    global labelFolderPath
    labelFolderPath.config(text=pathToWorkingFolder)


# Quit Program with shortcut
def quitProgram(event):
    sys.exit("ShortCut Quit: Eventmessage: " + str(event))


def test():
    print("TEST")
    global imageA
    global image_score_dict
    keyList = list(image_score_dict.keys())
    imageA = ImageTk.PhotoImage(Image.open(keyList[1]).resize((150, 150)))
    guiImageA = Label(tk_root, image=imageA)
    guiImageA.grid(row=5, column=0)

# tk root
tk_root = Tk()
tk_root.bind("<Control-q>", quitProgram)  # binding shortcut ctrl+q to function quitProgram()
tk_root.title("DeDup 0.1")

# Buttons
buttonToSetPathToWorkingFolder = Button(tk_root, text="Set Path To Working Directory",
                                        command=setPathToWorkingDirectory)
buttonToSetPathToWorkingFolder.grid(row=0, column=0)
buttonStartSearchForDupes = Button(tk_root, text="Start Search For Dupes", command=startThread)
buttonStartSearchForDupes.grid(row=2, column=0)
testButton = Button(tk_root, text="Test Me", command=test)
testButton.grid(row=7, column=0)

# Images
imageA = ImageTk.PhotoImage(Image.open("test2.png").resize((150, 150)))
guiImageA = Label(tk_root, image=imageA)
guiImageA.grid(row=5, column=0)

imageB = ImageTk.PhotoImage(Image.open("test2.png").resize((150, 150)))
guiImageB = Label(tk_root, image=imageB)
guiImageB.grid(row=5, column=1)

# Progressbar
progressBari = Progressbar(tk_root, orient="horizontal", length=300)
progressBari.grid(row=3, column=0, columnspan=2)
progressBarj = Progressbar(tk_root, orient="horizontal", length=300)
progressBarj.grid(row=4, column=0, columnspan=2)

# Textfield/Entry
thresholdTextfield = Entry(tk_root)
thresholdTextfield.insert(0, "70")
thresholdTextfield.grid(row=1, column=1)

# Label
labelFolderPath = Label(tk_root, text="Current Working Directory")
labelFolderPath.grid(row=0, column=1)
labelThreshold = Label(tk_root, text="Similarity Threshold in % ->")
labelThreshold.grid(row=1, column=0)
labelSimilarImagesFound = Label(tk_root, text="No Similar Pictures Found")
labelSimilarImagesFound.grid(row=2, column=1)

mainloop()
