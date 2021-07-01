import cv2

cv2.resizeWindow("enhanced", 640, 480)
image = cv2.imread('hsv4.png')
HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


def getpos(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 定义一个鼠标左键按下去的事件
        print(HSV[y, x])


cv2.imshow("imageHSV", HSV)
cv2.imshow('image', image)
cv2.setMouseCallback("imageHSV", getpos)
cv2.waitKey(0)
