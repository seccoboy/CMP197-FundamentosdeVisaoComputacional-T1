import numpy as np
from matplotlib import pyplot as plt
import cv2
import saveImage

image = cv2.imread('testimages/foto1_cap1.jpg')
imageOriginal = cv2.imread('testimages/foto1_gt.jpg')
click_list = []

def getClicks(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        click_list.append((x,y))
        print(x, ' ', y)
    return [x,y]

def getPoints():
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("output", 1080, 720)
    cv2.imshow('output', image)
    cv2.setMouseCallback('output', getClicks)
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
    return rect

def getRect():
    rect = np.zeros((4, 2), dtype = "float32")
    rect[0] = click_list[0]
    rect[1] = click_list[1]
    rect[2] = click_list[2]
    rect[3] = click_list[3]
    return rect

def resizeImage(image):
    width = imageOriginal.shape[1]
    height = imageOriginal.shape[0]
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    return resized

def fourPointTransform(image, pts):

    rect = orderPoints(pts)
    (topLeft, topRight, bottomRight, bottomLeft) = rect

    widthA = np.sqrt(((bottomRight[0] - bottomLeft[0]) ** 2) + ((bottomRight[1] - bottomLeft[1]) ** 2))
    widthB = np.sqrt(((topRight[0] - topLeft[0]) ** 2) + ((topRight[1] - topLeft[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((topRight[0] - bottomRight[0]) ** 2) + ((topRight[1] - bottomRight[1]) ** 2))
    heightB = np.sqrt(((topLeft[0] - bottomLeft[0]) ** 2) + ((topLeft[1] - bottomLeft[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, m, (maxWidth, maxHeight))
    return resizeImage(warped)

def plotImages(warped):
    cv2.namedWindow("Original", cv2.WINDOW_NORMAL)  
    cv2.imshow("Original", imageOriginal)
    cv2.namedWindow("Warped", cv2.WINDOW_NORMAL)
    cv2.imshow("Warped", warped)
    cv2.waitKey(0)

def plotGraphs(image):

    fig, ax = plt.subplots(1, 2)
    
    ax[0].hist(image.ravel(),bins = 256, range = [0,256]) 
    ax[1].hist(imageOriginal.ravel(),bins = 256, range = [0,256]) 
    
    fig.savefig("createdImages/histogramas.jpg")
    plt.show()
     
    fig, ax = plt.subplots(1, 2)

    color = ('b','g','r')
    for i,col in enumerate(color):
        warpedColorHistr = cv2.calcHist([image],[i],None,[256],[0,256])
        plt.xlim([0,256])
    ax[0].plot(warpedColorHistr, label="Warped Color Histogram")
        
    for i,col in enumerate(color):
        originalColorHistr = cv2.calcHist([imageOriginal],[i],None,[256],[0,256])
        plt.xlim([0,256])
    ax[1].plot(originalColorHistr,label="Original Color Histogram")

    ax[0].legend()
    ax[1].legend()
   
    fig.savefig("createdImages/colorHistograms.jpg")
   
    plt.show()
    
    cv2.waitKey(0)
    

def main():
    click_list = getPoints()
    rect = getRect()
    warped = fourPointTransform(image, rect)
    saveImage.main(warped, "Cortada")
    plotGraphs(warped)
    psnr = cv2.PSNR(warped, imageOriginal)
    print("PSNR: ",psnr)

    cv2.waitKey(0)

main()