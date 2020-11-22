from cv2 import *
from skimage.metrics import structural_similarity


class ImageSimilarityCalculator:
    imageSize = 350
    imageSize = (imageSize, imageSize)

    def ssim_calculation(self, pathToFileA, pathToFileB):
        imageA = cv2.imread(str(pathToFileA))
        imageB = cv2.imread(str(pathToFileB))
        imageA = cv2.resize(imageA, self.imageSize)
        imageB = cv2.resize(imageB, self.imageSize)
        (score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
        print("SSIM after reducing filesize: " + str(score))
        return score
