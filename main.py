import cv2
from image_similarity_calculator import ImageSimilarityCalculator
from skimage.metrics import structural_similarity
import glob
import json
import sys

print('Argument List:', str(sys.argv))

# Variables and Objects
pathToWorkingFolder = sys.argv[1]
global imageFilesInWorkingFolder
image_score_dict = {}
obj_imageSimilarityCalculator = ImageSimilarityCalculator()


# Searches through the designated work path and adds all files with specific post-fix to a list
def listOfAllImageFiles():
    global imageFilesInWorkingFolder
    imageFilesInWorkingFolder = ""  # CLean Up of the list
    imageFilesInWorkingFolder = [f for f in glob.glob(pathToWorkingFolder + "**/*.png", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpg", recursive=True)]
    imageFilesInWorkingFolder += [f for f in glob.glob(pathToWorkingFolder + "**/*.jpeg", recursive=True)]


# adds the path of imageA to the dictionary. imageA shall be the path and therefore an unique ID. this method
# is needed to access the "key" imageA and append the paths of similar images
def createNewKeyInDict(key, dict):
    dict[key] = []


# appends a value to the key of the dictionary
def addValueToDictKey(key, value, score, dict):
    dict[key].append((value, score))


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
    with open(pathToWorkingFolder + "/duplicates.json", 'w') as outfile:
        json.dump(image_score_dict, outfile)


# Essentialy takes all the filenames in the specified folder and runs it through the imageComparisonAlogrithm.
# It then fills a dictionary ith images and their duplicates
def startSearchForDupes():
    breakFlag = False
    imageSize = 200
    imageSize = (imageSize, imageSize)
    listOfAllImageFiles()
    for i in range(0, len(imageFilesInWorkingFolder)):
        imageA = cv2.imread(str(imageFilesInWorkingFolder[i]))
        try:
            imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        except:
            pass
        try:
            imageA = cv2.resize(imageA, imageSize)
        except Exception as e:
            print("Resizing not possible: " + str(imageA))
        for j in range(1 + i, len(imageFilesInWorkingFolder)):
            if not checkDictForExistingValues(imageFilesInWorkingFolder[j], image_score_dict):
                imageB = cv2.imread(str(imageFilesInWorkingFolder[j]))
                try:
                    imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
                except:
                    pass
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
    dumpToJSON()


startSearchForDupes()
