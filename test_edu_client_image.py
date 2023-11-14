import time
import cv2

#Display image in an OpenCV window
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Image', 640, 480)

while True:

    #Read image from MicroSD card
    image = cv2.imread('video.jpg', -1)
    cv2.imshow('Image', image)
    cv2.waitKey(1)
