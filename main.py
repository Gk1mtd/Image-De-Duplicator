# Eigentlich sollte ich die Score Daten in einer Datenbank speichern SQLite z.B.
# damit könnte zu jedem Bild-zu-Bild vergleich der Score gespeichert werden und damit Rechenzeit optimiert
# da die selben Bilder nicht n^n mal verglichen werden müssen
# import datetime
# from time import sleep
import _thread
# import datetime
# import multiprocessing
import os
from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import Progressbar
import cv2
from PIL import ImageTk, Image
from image_similarity_calculator import ImageSimilarityCalculator
from skimage.metrics import structural_similarity
import glob
import pprint
import json
import sys

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


# adds the path of imageA to the dictionary. imageA shall be the path and therefore an unique ID. this method
# is needed to access the "key" imageA and append the paths of similar images
def createNewKeyInDict(key, dict):
    dict[key] = []


# resets the dict to nothing
def clearDict(dict):
    # dict = {}
    dict.clear()


# appends a value to the key of the dictionary
def addValueToDictKey(key, value, score, dict):
    dict[key].append((value, score))
    # print("Added a new Value for Key: " + str(image_A) + " Value: " + str(similar_file_B))
    # pprint.pprint(image_score_dict)


def addValueToFilteredDictKey(key, value, dict):
    dict[key].append(value)


def checkDictForExistingKeys(key, dict):
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
    with open('data.json', 'w') as outfile:
        json.dump(image_score_dict, outfile)


def startThread():
    _thread.start_new_thread(startSearchForDupes, ("test1",))


# Essentialy takes all the filenames in the specified folder and runs it through the imageComparisonAlogrithm.
# It then fills a dictionary ith images and their duplicates
def startSearchForDupes(threadname="Damn Thread!"):  # Since i introduced Threads, now without it, the gui fucks up
    global breakFlag
    breakFlag = False
    imageSize = 200
    imageSize = (imageSize, imageSize)
    buttonStartSearchForDupes.grid_forget()  # hides Button
    buttonStopSearch.grid(row=1, column=0, columnspan=2)
    labelSimilarImagesFound.config(text="No Similar Pictures Found")
    progressBari['value'] = 0  # resets the progressbar
    progressBarj['value'] = 0  # resets the progressbar
    global number
    number = 0
    tk_root.update_idletasks()  # updates GUI
    clearDict(image_score_dict)
    listOfAllImageFiles()
    threshold = float(thresholdTextfield.get()) / 100
    similarImagesCounter = 0
    # start = datetime.datetime.now()
    for i in range(0, len(imageFilesInWorkingFolder)):
        if breakFlag:  # Escapes the search
            break
        imageA = cv2.imread(str(imageFilesInWorkingFolder[i]))
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        try:
            imageA = cv2.resize(imageA, imageSize)
        except Exception as e:
            print("Resizing not possible: " + str(imageA))
        setImageAInGUI(imageFilesInWorkingFolder[i])
        for j in range(1 + i, len(imageFilesInWorkingFolder)):
            if breakFlag:  # Escapes the search
                break
            setImageBInGUI(imageFilesInWorkingFolder[j])
            # labelCurrentFile.config(text="at File: " + str(imageFilesInWorkingFolder[j]))
            if not checkDictForExistingValues(imageFilesInWorkingFolder[j], image_score_dict):
                imageB = cv2.imread(str(imageFilesInWorkingFolder[j]))
                imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                try:
                    imageB = cv2.resize(imageB, imageSize)
                except Exception as e:
                    print("Resizing not possible: " + str(imageB))
                try:
                    (score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
                except Exception as e:
                    print("Error checking for similarities")

                if not checkDictForExistingKeys(imageFilesInWorkingFolder[i], image_score_dict):
                    createNewKeyInDict(imageFilesInWorkingFolder[i], image_score_dict)
                addValueToDictKey(imageFilesInWorkingFolder[i], imageFilesInWorkingFolder[j], score, image_score_dict)
            progressBarj['value'] = (100 * (j - i)) / (len(imageFilesInWorkingFolder) - i)  # shows single file progress
            if j == len(imageFilesInWorkingFolder) - 1:
                progressBarj['value'] = 100  # fills the progressbar complete, so it wont look like it stuck
            tk_root.update_idletasks()  # updates GUI
        progressBari['value'] = ((100 * (i + 1)) / len(imageFilesInWorkingFolder))  # shows total Progress
        tk_root.update_idletasks()  # updates GUI
        # dumpToJSON()  # saves all ocurences of smilar images right away // dont loose your progress bro
    dumpToJSON()
    buttonStopSearch.grid_forget()
    buttonStartSearchForDupes.grid(row=1, column=0, columnspan=2)  # shows the Search Button again
    # pprint.pprint(image_score_dict)
    # finish = datetime.datetime.now()
    # print(finish - start)


def setPathToWorkingDirectory():
    global pathToWorkingFolder
    pathToWorkingFolder = fd.askdirectory() + "/"
    # print("Set Working Directory to: " + pathToWorkingFolder)
    global labelFolderPath
    labelFolderPath.config(text=pathToWorkingFolder)


# Quit Program with shortcut
def quitProgram(event):
    sys.exit("ShortCut Quit: Eventmessage: " + str(event))


def setImageAInGUI(imageFromLoopA):
    global imageA
    imageA = ImageTk.PhotoImage(Image.open(imageFromLoopA).resize((150, 150)))
    guiImageA = Label(tk_root, image=imageA)
    guiImageA.grid(row=6, column=0)
    # print(imageFromLoopA)


def setImageBInGUI(imageFromLoopB):
    global imageB
    imageB = ImageTk.PhotoImage(Image.open(imageFromLoopB).resize((150, 150)))
    guiImageB = Label(tk_root, image=imageB)
    guiImageB.grid(row=6, column=1)


def stopSearch():
    global breakFlag
    breakFlag = True


def showNextDuplicates():
    global number
    number += 1


number = 0  # just for testing here, delte it at will


def calculateDuplicates():
    global number
    threshold = float(thresholdTextfield.get()) / 100
    global keyImage  # global machen, damit es auch von außen benutzbar wird, für tk_root
    global listOfValueImages

    with open('data.json') as json_file:
        data = json.load(json_file)  # parsed the ext json back to a dict

    filteredDict = {}

    # search through the data dict and makes a new one (called filteredDict), matching the threshold level
    for key in data:
        # pprint.pprint("item: " + str(key))
        createNewKeyInDict(key, filteredDict)
        for valueTupel in data[key]:
            # print("key: " + str(key) + " ### value: " + str(valueTupel))
            if valueTupel[1] >= threshold:
                addValueToFilteredDictKey(key, valueTupel[0], filteredDict)
                for x in filteredDict:
                    pass # print("#### values: " + str(filteredDict[x]))

    # clears filteredDict from empty keys
    popList = []
    for key in filteredDict:
        if not filteredDict.get(key):
            popList.append(key)
    for element in popList:
        filteredDict.pop(element)

    # clears dict of keys which are already values
    popList = []
    for key in filteredDict:
        for valueList in filteredDict.values():
            for value in valueList:
                if value == key:
                    popList.append(key)
    # makes content of poplist unique
    popList = set(popList)
    popList = list(popList)
    if popList != 0:
        for element in popList:
            filteredDict.pop(element)

    pprint.pprint(filteredDict)
    print("#########################")
    # clean up the filteredDict, so no key is also a value in another key

    # if not checkDictForExistingKeys(imageFilesInWorkingFolder[i], image_score_dict):
    #     createNewKeyInDict(imageFilesInWorkingFolder[i])
    # addValueToDictKey(imageFilesInWorkingFolder[i], imageFilesInWorkingFolder[j], score)

    # #os.remove("demofile.txt")
    # for i, key in enumerate(data):
    #     print(i, key)
    #
    # os.startfile(keyList[number]) # opens the path of the key
    # for i in list(data.get(keyList[number])): # open all occurences with same or higher threshold of score from key
    #     if float(data.get(keyList[number])[i][1]) >= threshold:
    #         os.startfile(data.get(keyList[number])[i][0])

    # keyImage = ImageTk.PhotoImage(Image.open(keyList[number]).resize((150, 150)))
    # guikeyImage = Label(tk_root, image=keyImage)
    # guikeyImage.grid(row=8, column=0)
    #
    # listOfValueImages = ImageTk.PhotoImage(Image.open(list(data.get(keyList[number]))[0]).resize((150, 150)))
    # guiListOfValueImages = Label(tk_root, image=listOfValueImages)
    # guiListOfValueImages.grid(row=8, column=1)


# GUI
# tk root
tk_root = Tk()
tk_root.bind("<Control-q>", quitProgram)  # binding shortcut ctrl+q to function quitProgram()
tk_root.title("DeDup 0.1")
# Gets both half the screen width/height and window width/height
positionRight = int((tk_root.winfo_screenwidth() / 2) - tk_root.winfo_reqwidth())
positionDown = int((tk_root.winfo_screenheight() / 2) - tk_root.winfo_reqheight())
# Positions the window in the center of the page.
tk_root.geometry("+{}+{}".format(positionRight, positionDown))

# Buttons
buttonToSetPathToWorkingFolder = Button(tk_root, text="Set Path To Working Directory",
                                        command=setPathToWorkingDirectory)
buttonToSetPathToWorkingFolder.grid(row=0, column=0)
buttonStartSearchForDupes = Button(tk_root, text="Calculate score of images", command=startThread)
buttonStartSearchForDupes.grid(row=1, column=0, columnspan=2)
buttonStopSearch = Button(tk_root, text="Stop calculating!", command=stopSearch)
buttonCalculateDuplicates = Button(tk_root, text="Filter Duplicates by threshold", command=calculateDuplicates)
buttonCalculateDuplicates.grid(row=7, column=0)
buttonShowNextDuplicates = Button(tk_root, text="Show Next Duplicates", command=showNextDuplicates)
buttonShowNextDuplicates.grid(row=8, column=0, columnspan=2)

# Progressbar
progressBari = Progressbar(tk_root, orient="horizontal", length=300)
progressBari.grid(row=2, column=0, columnspan=2)
progressBarj = Progressbar(tk_root, orient="horizontal", length=300)
progressBarj.grid(row=3, column=0, columnspan=2)

# Textfield/Entry
thresholdTextfield = Entry(tk_root)
thresholdTextfield.insert(0, "70")
thresholdTextfield.grid(row=6, column=1)

# Label
labelFolderPath = Label(tk_root, text="Current Working Directory")
labelFolderPath.grid(row=0, column=1)
labelThreshold = Label(tk_root, text="Similarity Threshold in % ->")
labelThreshold.grid(row=6, column=0)
labelCurrentFile = Label(tk_root, text="Current File", wraplength=300)
labelCurrentFile.grid(row=4, column=0, columnspan=2)
labelSimilarImagesFound = Label(tk_root, text="No Similar Pictures Found")
labelSimilarImagesFound.grid(row=7, column=1)

mainloop()
