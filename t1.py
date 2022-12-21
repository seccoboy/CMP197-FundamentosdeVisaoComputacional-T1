import numpy as np
from matplotlib import pyplot as plt
import argparse
import cv2

image = cv2.imread('testimages/foto1_cap2.jpg')
imageOriginal = cv2.imread('testimages/foto1_gt.jpg')
click_list = []

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        click_list.append((x,y))
        print(x, ' ', y)
    return [x,y]

def getPoints():
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("output", 1080, 720)
    cv2.imshow('output', image)
    cv2.setMouseCallback('output', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return click_list

def orderPoints(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):

    rect = orderPoints(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (maxWidth, maxHeight))
    # return the warped image
    return warped

def main():
    click_list = getPoints()
    rect = np.zeros((4, 2), dtype = "float32")
    rect[0] = click_list[0]
    rect[1] = click_list[1]
    rect[2] = click_list[2]
    rect[3] = click_list[3]
    warped = four_point_transform(image, rect)
    # show the original and warped images
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)  
    cv2.resizeWindow("Original", imageOriginal.shape[0], imageOriginal.shape[1])         
    cv2.imshow("Original", imageOriginal)
    cv2.namedWindow("Warped", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Warped", imageOriginal.shape[0], imageOriginal.shape[1])         
    cv2.imshow("Warped", warped)
    
    cv2.waitKey(0)

main()