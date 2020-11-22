from cv2 import *
from skimage.metrics import structural_similarity


class ImageSimilarityCalculator:

    def ssim_calculation(self, pathToFileA, pathToFileB):
        imageA = cv2.imread(str(pathToFileA))
        imageB = cv2.imread(str(pathToFileB))
        (score, diff) = structural_similarity(imageA, imageB, multichannel=True, full=True)
        print("SSIM: {}" + str(score))
        return score
