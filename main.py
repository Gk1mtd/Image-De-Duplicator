import os
from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import Progressbar
import json
import sys

# Variables and Objects
global jsonPath


def createNewKeyInDict(key, dict):
    dict[key] = []


def addValueToFilteredDictKey(key, value, dict):
    dict[key].append(value)


# Quit Program with shortcut
def quitProgram(event):
    sys.exit("ShortCut Quit: Eventmessage: " + str(event))


def LoadJsonFile():
    global jsonPath
    jsonPath = str(fd.askopenfilename())


def calculateDuplicates():
    threshold = float(thresholdTextfield.get()) / 100
    global keyImage  # global machen, damit es auch von außen benutzbar wird, für tk_root
    global listOfValueImages

    with open(jsonPath) as json_file:
        data = json.load(json_file)  # parsed the ext json back to a dict

    global filteredDict
    filteredDict = {}

    # search through the data dict and makes a new one (called filteredDict), matching the threshold level
    count = 0
    dataLenght = 0
    for key in data:
        dataLenght += 1
    for key in data:
        count += 1
        createNewKeyInDict(key, filteredDict)
        progressBari['value'] = (count * 100) / dataLenght  # shows total Progress
        tk_root.update_idletasks()  # updates GUI
        for valueTupel in data[key]:
            if valueTupel[1] >= threshold:
                addValueToFilteredDictKey(key, valueTupel[0], filteredDict)
                for x in filteredDict:
                    pass

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

    # counts duplicates
    count = 0
    for x in filteredDict.values():
        for y in x:
            count += 1
    labelSimilarImagesFound.config(text=str(len(filteredDict.values())) + " images have " + str(count) + " duplicates")

    # **********listbox
    listvariable = list(filteredDict.keys())
    listvariable = StringVar(value=listvariable)

    global listbox
    listbox = Listbox(tk_root, listvariable=listvariable, height=20, width=80)
    listbox.grid(row=9, column=0, columnspan=2)
    listbox.bind('<<ListboxSelect>>', items_selected)

    # pprint.pprint(filteredDict)
    # print("#########################")


def items_selected(event):
    # get selected indices
    selected_indices = listbox.curselection()
    # get selected items
    selected_langs = ",".join([listbox.get(i) for i in selected_indices])
    try:
        os.startfile(selected_langs)
    except:
        pass
    keyitem = filteredDict.get(selected_langs)
    try:
        for i in keyitem:
            os.startfile(i)
    except:
        pass


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
buttonCalculateDuplicates = Button(tk_root, text="Filter Duplicates by threshold", command=calculateDuplicates)
buttonCalculateDuplicates.grid(row=2, column=0)
buttonLoadJsonFile = Button(tk_root, text="Load Json File", command=LoadJsonFile)
buttonLoadJsonFile.grid(row=0, column=0, columnspan=2)

# Progressbar
progressBari = Progressbar(tk_root, orient="horizontal", length=300)
progressBari.grid(row=3, column=0, columnspan=2)

# Textfield/Entry
thresholdTextfield = Entry(tk_root)
thresholdTextfield.insert(0, "70")
thresholdTextfield.grid(row=1, column=1)

# Label
labelThreshold = Label(tk_root, text="Similarity Threshold in % ->")
labelThreshold.grid(row=1, column=0)
labelSimilarImagesFound = Label(tk_root, text="No Similar Pictures Found")
labelSimilarImagesFound.grid(row=2, column=1)

mainloop()
