
import cv2, numpy as np

img = cv2.imread('testimages/foto1_cap1.jpg')

click_list = []

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        click_list.append((x,y))
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
    return [x,y]

def main():
    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("output", 1080, 720)
    cv2.imshow('output', img)
    cv2.setMouseCallback('output', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return click_list

main()