import datetime
from image_similarity_calculator import ImageSimilarityCalculator
from gui import GUI


obj_gui = GUI()

start = datetime.datetime.now()
# to calculate SSIM (similarity) of to pictures given as setImageA() and setImageB()
obj_imageSimilarityCalculator = ImageSimilarityCalculator()
obj_imageSimilarityCalculator.ssim_calculation("original.png", "other_image.jpg")

finish = datetime.datetime.now()
print(finish-start)