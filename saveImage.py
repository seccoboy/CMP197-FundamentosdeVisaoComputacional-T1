import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def main(image, name):
    
    cv.imwrite("createdImages/" +name+".jpg", image)
