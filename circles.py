import cv2
import numpy as np
# Read image as gray-scale
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
print(check) #prints true as long as the webcam is running
print(frame) #prints matrix values of each framecd 
 cv2.imshow("Capturing", frame)
img = cv2.imread('circles.png', cv2.IMREAD_COLOR)
# Convert to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image to reduce noise
img_blur = cv2.medianBlur(gray, 5)
# Apply hough transform on the image
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/64, param1=200, param2=10, minRadius=5, maxRadius=30)
# Draw detected circles
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        print("Circle found")
        # Draw outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Draw inner circle
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
    cv2.imshow("Evv",img)
    cv2.waitKey()
