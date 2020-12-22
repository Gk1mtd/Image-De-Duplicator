from cv2 import *
from skimage.metrics import structural_similarity


class ImageSimilarityCalculator:
    imageSize = 350
    imageSize = (imageSize, imageSize)

    def ssim_calculation(self, pathToFileA, pathToFileB, treshhold):
        imageA = cv2.imread(str(pathToFileA))
        imageB = cv2.imread(str(pathToFileB))
        imageA = cv2.resize(imageA, self.imageSize)
        imageB = cv2.resize(imageB, self.imageSize)
        imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        (score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
        if score >= treshhold:
            print("SSIM after reducing filesize: " + str(score))
            print("ImageA was: " + str(pathToFileA) + " | ImageB was: " + str(pathToFileB))
            return score
