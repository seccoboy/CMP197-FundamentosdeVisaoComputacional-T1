
import cv2, numpy as np

img = cv2.imread('testImages/test.png', 1)
click_list = []

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        click_list.append((x,y))
        print(x, ' ', y)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        cv2.imshow('image', img)
    return [x,y]

def main():
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    for position in click_list:
        x, y = position[0], position[1]
        print(x,y)
    cv2.destroyAllWindows()
main()